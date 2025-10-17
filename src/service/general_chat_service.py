# -*- coding: utf-8 -*-
import json
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import sys
import os
import glob
import re
import tarfile
from datetime import datetime
from typing import Optional, List
from openai import OpenAI
import base64
import logging
import gzip

# Load context data (caching to avoid repeated file reads)
_CONTEXT_LIST = []

def load_contexts(json_path: str = None):
    """Load contexts from JSON file"""
    global _CONTEXT_LIST
    if json_path is None:
        # Build path relative to the current script location
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(current_dir, "../../child_contexts.json")
    
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["contexts"]


def detect_context(
        user_input: str,
        child_age: Optional[int] = None,
        min_score: int = 1
) -> Optional[str]:
    """
    根据用户输入自动匹配最相关的情境指令
    
    Args:
        user_input (str): 用户的原始消息
        child_age (int, optional): 孩子年龄（用于过滤不匹配年龄段的情境）
        min_score (int): 最低匹配关键词数量（默认1个即触发）

    Returns:
        str or None: 匹配到的情境指令文本，如"小朋友害怕晚上一个人睡觉"
    """
    if not user_input.strip():
        return None

    # 标准化输入（转小写，保留中文/英文/数字）
    clean_input = re.sub(r"[^\w\s\u4e00-\u9fff]", " ", user_input.lower())
    words = set(clean_input.split())

    best_match = None
    best_score = 0

    for ctx in _CONTEXT_LIST:
        # 如果提供了年龄，跳过不匹配年龄段的情境
        if child_age is not None:
            min_age, max_age = ctx["age_range"]
            if not (min_age <= child_age <= max_age):
                continue

        # 计算匹配关键词数量
        matched_keywords = [kw for kw in ctx["keywords"] if kw in user_input]
        score = len(matched_keywords)

        # 优先选择匹配度更高的；若相同，优先更具体的情境（关键词多的）
        if score >= min_score and score > best_score:
            best_score = score
            best_match = ctx["instruction"]

    return best_match


# Try to import tokenizer, with fallback
try:
    from dashscope import get_tokenizer
    DASHSCOPE_AVAILABLE = True
except ImportError:
    DASHSCOPE_AVAILABLE = False
    get_tokenizer = None

# Try to import ali_voice, with fallback
try:
    from .ali_voice import AliVoiceClient
    ALI_VOICE_AVAILABLE = True
except ImportError:
    try:
        from ali_voice import AliVoiceClient
        ALI_VOICE_AVAILABLE = True
    except ImportError:
        ALI_VOICE_AVAILABLE = False
        AliVoiceClient = None

# Store the model configuration in memory
MODEL_CONFIGS = {}
CHAT_HISTORY = {}
CHARACTER_PROMPTS = {}
CHARACTER_OPENING_MESSAGES = {}

# Initialize AliVoice client
ALI_VOICE_CLIENT = None


class RotatingCompressedLogHandler(logging.Handler):
    """
    Custom logging handler that:
    1. Maintains active log files as original names (qs.txt, web_chat.log)
    2. Rotates logs by date (creates new file each day)
    3. Rotates logs by size (creates new file when size exceeds limit)
    4. Compresses old log files to .tar.gz format with timestamps
    """
    def __init__(self, log_file_path, max_bytes=5*1024*1024, backup_count=5):
        super().__init__()
        self.log_file_path = log_file_path  # Full path for the active log file
        self.max_bytes = max_bytes  # 5MB default
        self.backup_count = backup_count
        self.current_file_handle = None
        self.current_log_date = None
        self.current_file_size = 0
        
        # Extract directory and base name from the path
        self.log_dir = os.path.dirname(log_file_path)
        self.base_name = os.path.basename(log_file_path)  # e.g., "qs.txt" or "web_chat.log"
        self.base_name_no_ext, self.ext = os.path.splitext(self.base_name)  # e.g., "qs" and ".txt"
        
        # Create logs directory if it doesn't exist
        os.makedirs(self.log_dir, exist_ok=True)
        
        # Initialize the handler
        self._ensure_current_log_exists()

    def emit(self, record):
        """
        Emit a record by writing it to the appropriate log file
        """
        try:
            # Check if we need to rotate the log file
            self._check_and_rotate()
            
            # Write the log record to the current active log file
            if self.current_file_handle:
                msg = self.format(record)
                self.current_file_handle.write(msg + '\n')
                self.current_file_handle.flush()
                
                # Update the current file size
                self.current_file_size += len(msg.encode('utf-8')) + 1  # +1 for newline
                
        except Exception as e:
            self.handleError(record)

    def _ensure_current_log_exists(self):
        """
        Ensure the current log file exists and open its handle
        """
        # Check if the current log file exists, create it if it doesn't
        if not os.path.exists(self.log_file_path):
            # Create the file if it doesn't exist
            os.makedirs(self.log_dir, exist_ok=True)
            # Create the file with empty content
            with open(self.log_file_path, 'a', encoding='utf-8'):
                pass
        
        # Open the current log file
        self.current_file_handle = open(self.log_file_path, 'a', encoding='utf-8')
        
        # Get the current date for tracking
        self.current_log_date = datetime.now().strftime('%Y%m%d')
        
        # Get the current file size
        self.current_file_size = os.path.getsize(self.log_file_path)

    def _check_and_rotate(self):
        """
        Check if we need to rotate the log file based on date or size
        """
        current_date = datetime.now().strftime('%Y%m%d')
        
        # Check if we need to rotate based on date
        should_rotate_by_date = (
            self.current_log_date is not None 
            and self.current_log_date != current_date
        )
        
        # Check if we need to rotate based on size
        should_rotate_by_size = (
            self.current_file_size >= self.max_bytes
        )
        
        # If we need to rotate for any reason
        if should_rotate_by_date or should_rotate_by_size:
            self._rotate_current_log()

    def _rotate_current_log(self):
        """
        Rotate the current active log file to a timestamped archive and start a new active log file
        """
        if self.current_file_handle:
            # Close current file handle before rotation
            self.current_file_handle.close()
            
            # Rename the current log file to a timestamped name before compression
            current_date = datetime.now().strftime('%Y%m%d')
            timestamp = datetime.now().strftime('%y%m%d%H%M%S')  # e.g., 2510132333
            
            # Create archive filename with timestamp
            archive_filename = f"{self.base_name_no_ext}{timestamp}{self.ext}"
            archive_path = os.path.join(self.log_dir, archive_filename)
            
            # Rename the current log file to the archive name
            os.rename(self.log_file_path, archive_path)
            
            # Compress the archived log file
            self._compress_log_file(archive_path, archive_filename)
            
            # Create a fresh active log file with original name
            self.current_file_handle = open(self.log_file_path, 'a', encoding='utf-8')
            self.current_log_date = current_date
            self.current_file_size = 0

    def _compress_log_file(self, file_path, original_filename):
        """
        Compress the specified log file to .tar.gz format
        """
        if os.path.exists(file_path):
            # Create compressed filename
            dir_path = os.path.dirname(file_path)
            base_name = os.path.splitext(original_filename)[0]  # Get name without extension
            compressed_filename = f"{base_name}.tar.gz"
            compressed_path = os.path.join(dir_path, compressed_filename)
            
            # Create a tar.gz archive containing the log file
            with tarfile.open(compressed_path, "w:gz") as tar:
                tar.add(file_path, arcname=original_filename)
            
            # Remove the original uncompressed file after compression
            os.remove(file_path)
            
            # Clean up old backup files if we exceed backup count
            self._clean_old_backups()

    def _clean_old_backups(self):
        """
        Clean up old backup files to maintain backup count
        """
        # Find all log files (compressed and uncompressed) for this log series
        pattern = os.path.join(self.log_dir, f"{self.base_name_no_ext}*")
        
        # Get all matching files and sort by modification time (oldest first)
        all_log_files = []
        for file in glob.glob(pattern):
            # Check if it's a log file for the same base name
            filename = os.path.basename(file)
            if filename.startswith(self.base_name_no_ext):
                # Exclude the current active log file
                if file != self.log_file_path:
                    all_log_files.append((os.path.getmtime(file), file))
        
        # Sort by modification time (oldest first)
        all_log_files.sort(key=lambda x: x[0])
        
        # Keep only the most recent files up to backup_count
        if len(all_log_files) > self.backup_count:
            for _, old_file in all_log_files[:-self.backup_count]:
                try:
                    if old_file.endswith('.tar.gz'):
                        # For compressed files, just remove them
                        os.remove(old_file)
                    else:
                        # For uncompressed archived files, compress then remove
                        dir_path = os.path.dirname(old_file)
                        filename = os.path.basename(old_file)
                        base_name = os.path.splitext(filename)[0]
                        compressed_filename = f"{base_name}.tar.gz"
                        compressed_path = os.path.join(dir_path, compressed_filename)
                        
                        # Compress the file before removing
                        with tarfile.open(compressed_path, "w:gz") as tar:
                            tar.add(old_file, arcname=filename)
                        
                        # Remove the original uncompressed file
                        os.remove(old_file)
                except OSError:
                    pass  # Ignore errors when removing old files

    def close(self):
        """
        Close the current log file
        """
        if self.current_file_handle:
            self.current_file_handle.close()
            self.current_file_handle = None
        super().close()




# Define log file paths
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
LOG_FILE_PATH = os.path.join(current_dir, "../../result/logs/qs.txt")

# Set up logging for voice operations with rotation
VOICE_LOG_PATH = os.path.join(current_dir, "../../result/logs/web_chat.log")

# Create custom handlers with rotation and compression
QS_HANDLER = RotatingCompressedLogHandler(LOG_FILE_PATH)
VOICE_HANDLER = RotatingCompressedLogHandler(VOICE_LOG_PATH)

# Set up logging with custom handlers
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        VOICE_HANDLER,  # Custom handler for web chat logs
        logging.StreamHandler()  # Also log to console
    ]
)
VOICE_LOGGER = logging.getLogger(__name__)

# Create a separate logger for the qs.txt logging
QS_LOGGER = logging.getLogger('qs_logger')
QS_LOGGER.setLevel(logging.INFO)
QS_LOGGER.addHandler(QS_HANDLER)
# Prevent propagation to root logger to avoid duplication
QS_LOGGER.propagate = False

def load_character_prompts():
    """Load all character prompts"""
    global CHARACTER_PROMPTS
    
    # Try to load Peppa Pig character
    try:
        from .peppa_pig_character import create_peppa_pig_prompt
        CHARACTER_PROMPTS['peppa_pig'] = create_peppa_pig_prompt()
    except ImportError:
        try:
            from peppa_pig_character import create_peppa_pig_prompt
            CHARACTER_PROMPTS['peppa_pig'] = create_peppa_pig_prompt()
        except ImportError:
            print("Peppa Pig character module not found")
    
    # Try to load Nezha character
    try:
        from .nezha_character import create_nezha_prompt
        CHARACTER_PROMPTS['nezha'] = create_nezha_prompt()
    except ImportError:
        try:
            from nezha_character import create_nezha_prompt
            CHARACTER_PROMPTS['nezha'] = create_nezha_prompt()
        except ImportError:
            print("Nezha character module not found")
    
    # Try to load General character
    try:
        from .general_character import create_general_prompt
        CHARACTER_PROMPTS['general'] = create_general_prompt()
    except ImportError:
        try:
            from general_character import create_general_prompt
            CHARACTER_PROMPTS['general'] = create_general_prompt()
        except ImportError:
            print("General character module not found")
    
    # Set default character if none loaded
    if not CHARACTER_PROMPTS:
        # Create a default general prompt
        CHARACTER_PROMPTS['general'] = """
        你是一个友好的聊天伙伴，可以和小朋友聊天、分享故事、回答问题。请用温和友善的语气进行交流。
        - 态度友善、耐心
        - 语言简洁易懂
        - 回答要积极正面
        """

def load_character_opening_messages():
    """Load role-specific opening messages for each character"""
    global CHARACTER_OPENING_MESSAGES
    
    # Peppa Pig opening message - for young children, focused on games and fun
    CHARACTER_OPENING_MESSAGES['peppa_pig'] = "哼哼！我是爱跳泥坑的小猪佩奇！我们一起玩游戏吧？还是一起去冒险？"
    
    # Nezha opening message - for 7-12 year olds, focused on secrets, emotional support, and knowledge
    CHARACTER_OPENING_MESSAGES['nezha'] = "嘿！我是哪吒！你的秘密我守护，超酷知识我分享——今天想聊心情，还是探索世界？"
    
    # General character opening message - for broad age range, focused on friendship and Q&A
    CHARACTER_OPENING_MESSAGES['general'] = "你好呀！我是你的好伙伴！今天想轻松聊天、一起解谜闯关，还是探索科学、历史、甚至冷知识？"

def load_model_config(config_path):
    """Load model configuration from JSON file"""
    with open(config_path, 'r', encoding='utf-8') as f:
        configs = json.load(f)
    
    # If it's a single config object, convert to list
    if isinstance(configs, dict):
        configs = [configs]
    
    # Convert to a dictionary with config names as keys
    config_dict = {}
    for config in configs:
        config_dict[config.get('config_name')] = config
    
    return config_dict



def extract_episodes_from_content(content):
    """Extract individual episodes from the content using markdown headers."""
    import re
    
    # Split content by episode headers (## followed by episode number and title)
    episodes = re.split(r'\n##\s+', content)
    
    # Remove the first element which is just text before the first episode
    if episodes and not episodes[0].strip().startswith("0"):
        episodes.pop(0)
    
    # Add back the header to each episode
    formatted_episodes = []
    for episode in episodes:
        if episode.strip():
            # Add back the ## header
            formatted_episode = "## " + episode
            formatted_episodes.append(formatted_episode)
    
    return formatted_episodes





def get_character_prompt(character_name):
    """Get the prompt for the specified character"""
    if character_name in CHARACTER_PROMPTS:
        return CHARACTER_PROMPTS[character_name]
    else:
        # Return the first available character prompt as default
        if CHARACTER_PROMPTS:
            return list(CHARACTER_PROMPTS.values())[0]
        else:
            # Default fallback prompt
            return """
            你是一个友好的聊天伙伴，可以和小朋友聊天、分享故事、回答问题。请用温和友善的语气进行交流。
            - 态度友善、耐心
            - 语言简洁易懂
            - 回答要积极正面
            """


def count_tokens(text, model_name="qwen-turbo"):
    """
    Count tokens in the given text using appropriate tokenizer.
    Falls back to character count if no tokenizer is available.
    """
    # Try DashScope tokenizer first (as per sample implementation)
    if DASHSCOPE_AVAILABLE:
        try:
            tokenizer = get_tokenizer(model_name)
            tokens = tokenizer.encode(text)
            return len(tokens)
        except Exception:
            # If DashScope fails, fall back to alternative methods
            pass
    
    # Try tiktoken as alternative
    try:
        import tiktoken
        # Try to get encoding for the specific model, fallback to gpt-3.5-turbo
        try:
            encoding = tiktoken.encoding_for_model(model_name)
        except KeyError:
            # If model not found, use a common encoding
            encoding = tiktoken.get_encoding("cl100k_base")
        tokens = encoding.encode(text)
        return len(tokens)
    except ImportError:
        # If tiktoken not available, fall back to character count
        pass
    
    # Ultimate fallback: character count (less accurate but always works)
    return len(text.encode('utf-8'))

class GeneralChatHandler(BaseHTTPRequestHandler):
    
    def get_character_history_key(self, character_name):
        """Generate a unique key for character history including client identifier"""
        # Extract client identifier from request headers or use client IP
        client_id = self._get_client_identifier()
        return f"history_{character_name}_{client_id}"
    
    def _get_client_identifier(self):
        """Extract client identifier from request headers or use IP address"""
        # Check for custom client identifier in headers
        custom_client_id = self.headers.get('X-Client-ID') or self.headers.get('X-Session-ID')
        if custom_client_id:
            return custom_client_id
        
        # Fallback to using the client's IP address
        client_ip = self.client_address[0] if hasattr(self.client_address, '__getitem__') else 'unknown'
        
        # Sanitize IP address to be safe for use in dict keys
        safe_client_id = client_ip.replace('.', '_').replace(':', '_')
        return f"ip_{safe_client_id}"
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            html_content = self.get_html_content()
            self.wfile.write(html_content.encode('utf-8'))
            
        elif parsed_path.path == '/models':
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            
            response = {"models": list(MODEL_CONFIGS.keys())}
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            
        elif parsed_path.path == '/characters':
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            
            response = {"characters": list(CHARACTER_PROMPTS.keys())}
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            
        elif parsed_path.path == '/history':
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            
            # Get character name from query parameter, default to first character
            parsed_query = parse_qs(urlparse(self.path).query)
            character_name = parsed_query.get('character', [list(CHARACTER_PROMPTS.keys())[0] if CHARACTER_PROMPTS else 'general'])[0]
            history_key = self.get_character_history_key(character_name)
            
            if history_key not in CHAT_HISTORY:
                CHAT_HISTORY[history_key] = []
            
            response = {"history": CHAT_HISTORY[history_key]}
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
        
        elif parsed_path.path == '/openings':
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            
            # Return all character opening messages
            response = {"openings": CHARACTER_OPENING_MESSAGES}
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            
        elif parsed_path.path == '/opening':
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            
            # Get character name from query parameter, default to first character
            parsed_query = parse_qs(urlparse(self.path).query)
            character_name = parsed_query.get('character', [list(CHARACTER_PROMPTS.keys())[0] if CHARACTER_PROMPTS else 'general'])[0]
            
            # Return opening message for specific character
            opening_message = CHARACTER_OPENING_MESSAGES.get(character_name, "")
            response = {"opening": opening_message, "character": character_name}
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        parsed_path = urlparse(self.path)

        if parsed_path.path == '/chat':
            # Parse the request data
            try:
                # Check Content-Type to determine if it's application/json or raw audio data
                content_type = self.headers.get('Content-Type', '')
                
                if content_type.startswith('audio/'):
                    # Handle raw audio data as byte stream
                    # Re-read the raw binary data instead of the text we already read
                    content_length = int(self.headers['Content-Length'])
                    audio_bytes = self.rfile.read(content_length)
                    
                    # Initialize default values
                    user_message = ''
                    model_config_name = 'qwen3-32B'
                    custom_prompt = None
                    character_name = 'peppa_pig'  # Default character
                    tts_voice = 'aitong'  # Default voice for TTS
                    tts_format = 'wav'  # Default TTS format
                    tts_sample_rate = 16000  # Default TTS sample rate
                    asr_format = 'wav'  # Default ASR format
                    asr_sample_rate = 16000  # Default ASR sample rate
                    audio_data = audio_bytes  # Store raw audio bytes
                    
                    # Log the request for audio content type
                    VOICE_LOGGER.info(f"Received audio request with Content-Type: {content_type}, size: {len(audio_bytes)} bytes")
                else:
                    # Handle JSON data
                    request_data = json.loads(post_data)
                    user_message = request_data.get('message', '')
                    audio_data = request_data.get('audio', None)  # Audio data as base64 string
                    model_config_name = request_data.get('model_config_name', 'qwen3-8B')
                    custom_prompt = request_data.get('custom_prompt', None)
                    character_name = request_data.get('character', 'peppa_pig')  # Default to peppa_pig
                    # Add support for voice parameter for TTS
                    tts_voice = request_data.get('voice', 'aitong')  # Default to 'aitong' if not specified
                    # Add support for TTS parameters
                    tts_format = request_data.get('tts_format', 'wav')  # Default TTS format
                    tts_sample_rate = request_data.get('tts_sample_rate', 16000)  # Default TTS sample rate
                    # Add support for ASR parameters
                    asr_format = request_data.get('asr_format', 'wav')  # Default ASR format
                    asr_sample_rate = request_data.get('asr_sample_rate', 16000)  # Default ASR sample rate
                    
                    # Log the JSON request body, but simplify audio data to avoid long base64 strings
                    log_request_data = request_data.copy()
                    if 'audio' in log_request_data and log_request_data['audio']:
                        log_request_data['audio'] = 'not null'  # Replace long base64 string with 'not null'
                    VOICE_LOGGER.info(f"Received JSON request: {json.dumps(log_request_data, ensure_ascii=False)}")
                    
            except json.JSONDecodeError:
                self.send_response(400)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                response = {"error": "Invalid JSON"}
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                return
            except Exception as e:
                self.send_response(400)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                response = {"error": f"Error parsing request: {str(e)}"}
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                return
            
            # Validate character name
            if character_name not in CHARACTER_PROMPTS:
                # Use the first available character as default
                character_name = list(CHARACTER_PROMPTS.keys())[0] if CHARACTER_PROMPTS else 'general'
            
            # If audio data is provided, convert it to text using AliVoice
            if audio_data and ALI_VOICE_CLIENT:
                try:
                    VOICE_LOGGER.info(f"Starting speech-to-text conversion, audio data type: {type(audio_data)}, size: {len(audio_data) if hasattr(audio_data, '__len__') else 'unknown'}")
                    
                    # If audio_data is a base64 string, decode it to bytes
                    if isinstance(audio_data, str):
                        audio_bytes = base64.b64decode(audio_data)
                        VOICE_LOGGER.info(f"Decoded base64 audio data, size: {len(audio_bytes)} bytes")
                    else:
                        audio_bytes = audio_data
                        VOICE_LOGGER.info(f"Using raw audio bytes, size: {len(audio_bytes)} bytes")
                    
                    # Convert speech to text
                    asr_result = ALI_VOICE_CLIENT.speech_to_text(
                        audio_data=audio_bytes,
                        format=asr_format,  # Use format from request
                        sample_rate=asr_sample_rate  # Use sample rate from request
                    )
                    
                    if asr_result["success"]:
                        # Log the ASR result before updating user_message
                        original_message = user_message  # Store original
                        user_message = asr_result["text"]
                        VOICE_LOGGER.info(f"Speech-to-text conversion successful: '{user_message}' (was: '{original_message}')")
                    else:
                        VOICE_LOGGER.error(f"ASR failed: {asr_result['error']}")
                        # If ASR fails, continue with the original user_message if any
                        VOICE_LOGGER.info(f"Continuing with original message: '{user_message}' after ASR failure")
                except Exception as e:
                    VOICE_LOGGER.error(f"Error in speech-to-text conversion: {e}")
                    import traceback
                    VOICE_LOGGER.error(f"Full traceback: {traceback.format_exc()}")
                    # Continue with original user_message if any
                    VOICE_LOGGER.info(f"Continuing with original message: '{user_message}' after ASR exception")
            
            # Validate model config
            if model_config_name not in MODEL_CONFIGS:
                self.send_response(400)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                response = {"error": "Model config '{}' not found".format(model_config_name)}
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                return
            
            # Get the model config
            model_config = MODEL_CONFIGS[model_config_name]
            
            # Get character history
            history_key = self.get_character_history_key(character_name)
            if history_key not in CHAT_HISTORY:
                CHAT_HISTORY[history_key] = []
            
            # Use custom prompt if provided, otherwise use character's default prompt
            system_prompt = custom_prompt if custom_prompt else get_character_prompt(character_name)
            
            # Add user message to history
            CHAT_HISTORY[history_key].append({"role": "user", "content": user_message})
            
            # Detect context based on user input
            context_instruction = detect_context(user_message)
            
            # Log context detection result
            if context_instruction:
                VOICE_LOGGER.info(f"Context detected for user message '{user_message[:50]}...': {context_instruction}")
            else:
                VOICE_LOGGER.info(f"No context detected for user message: '{user_message[:50]}...'")
            
            # Prepare messages with system prompt and context if found
            system_prompt = get_character_prompt(character_name)
            
            # If context is detected, append it to the system prompt
            if context_instruction:
                system_prompt = f"{system_prompt}\n\n当前情境：{context_instruction}\n请根据这个情境，用适配角色的方式回应小朋友。"
            
            # Log the actual system prompt that will be sent to the model
            VOICE_LOGGER.info(f"System prompt sent to model: {system_prompt}")
            
            # Prepare the conversation history for the API call
            # Include system prompt as the first message
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add all previous conversation history (maintain full context unless too long)
            # Start from the beginning of history, but truncate if too long
            history_to_send = []
            for msg in CHAT_HISTORY[history_key]:
                if msg["role"] != "system":  # Exclude system message from history since we add it separately
                    history_to_send.append({"role": msg["role"], "content": msg["content"]})
            
            # Check if history is too long (by counting tokens/characters), and if so, truncate oldest entries
            # For simplicity, we'll count characters (in real implementation you might want to count tokens)
            total_content_length = sum(len(str(msg["content"])) for msg in history_to_send)
            max_content_length = 3000  # Adjust this limit as needed - 3000 characters as per requirement
            
            if total_content_length > max_content_length:
                # Remove oldest messages until under the limit
                while len(history_to_send) > 2 and total_content_length > max_content_length:
                    history_to_send.pop(0)  # Remove oldest message
                    total_content_length = sum(len(str(msg["content"])) for msg in history_to_send)
            
            messages.extend(history_to_send)
            
            # Log the full message history that will be sent to the model
            VOICE_LOGGER.info(f"Full conversation history sent to model: {json.dumps(messages, ensure_ascii=False, indent=2)}")
            
            # Generate response using the selected model
            try:
                model_config = MODEL_CONFIGS[model_config_name]
                model_type = model_config.get("model_type", "openai_chat")
                model_name = model_config["model_name"]
                api_key = model_config["api_key"]
                
                # Get base URL from config
                base_url = model_config.get("client_args", {}).get("base_url", "https://api.openai.com/v1")
                
                # Create OpenAI client with appropriate configuration
                client = OpenAI(
                    api_key=api_key,
                    base_url=base_url
                )
                
                # Check if this is a DashScope model that requires special parameters
                if model_type == "dashscope_chat" or "qwen" in model_name.lower():
                    # For DashScope models, we need to include additional parameters
                    response = client.chat.completions.create(
                        model=model_name,
                        messages=messages,
                        timeout=60,  # Add timeout to avoid hanging
                        max_tokens=100,  # Limit response length to keep it concise like original script
                        temperature=0.5,  # Slightly reduce randomness to encourage shorter responses
                        extra_body={
                            "enable_thinking": False,  # Required for DashScope non-streaming calls
                            "max_tokens": 100  # Also set max tokens in extra_body for DashScope to keep responses short
                        }
                    )
                else:
                    # For other models (like OpenAI-compatible ones)
                    response = client.chat.completions.create(
                        model=model_name,
                        messages=messages,
                        timeout=60,  # Add timeout to avoid hanging
                        max_tokens=100,  # Limit response length to keep it concise like original script
                        temperature=0.5  # Slightly reduce randomness to encourage shorter responses
                    )
                
                response_content = response.choices[0].message.content
                
                # Count tokens in input (full message history including system prompt) and output (assistant response)
                # Convert the messages list to a single string for token counting
                full_input_text = ""
                for msg in messages:
                    full_input_text += f"{msg['role']}: {msg['content']}\n"
                
                input_token_count = count_tokens(full_input_text, model_name)
                output_token_count = count_tokens(response_content, model_name)
                
                # Log token count information
                VOICE_LOGGER.info(f"Token counts - Input: {input_token_count}, Output: {output_token_count}, Model: {model_name}, Character: {character_name}")
                
                # Add assistant's response to history
                CHAT_HISTORY[history_key].append({"role": "assistant", "content": response_content})
                
                # Check if history is too long (by counting characters), and if so, truncate oldest entries
                # For simplicity, we'll count characters (in real implementation you might want to count tokens)
                total_content_length = sum(len(str(msg["content"])) for msg in CHAT_HISTORY[history_key])
                max_content_length = 3000  # Adjust this limit as needed - 3000 characters as per requirement
                
                if total_content_length > max_content_length:
                    # Remove oldest messages until under the limit
                    while len(CHAT_HISTORY[history_key]) > 2 and total_content_length > max_content_length:
                        CHAT_HISTORY[history_key].pop(0)  # Remove oldest message
                        total_content_length = sum(len(str(msg["content"])) for msg in CHAT_HISTORY[history_key])
                
                # Log the conversation to file with token counts and client ID
                client_id = self._get_client_identifier()
                self.log_conversation(user_message, response_content, model_config_name, input_token_count, output_token_count, character_name, client_id)
                
                # Convert text response to speech using AliVoice
                audio_response = ""
                if ALI_VOICE_CLIENT:
                    try:
                        # Use voice from request parameter, default to 'aitong' if not specified
                        voice = tts_voice
                        
                        VOICE_LOGGER.info(f"Starting text-to-speech conversion for response: '{response_content[:50]}...', voice: {voice}")
                        tts_result = ALI_VOICE_CLIENT.text_to_speech(
                            text=response_content,
                            voice=voice,
                            format=tts_format,  # Use format from request
                            sample_rate=tts_sample_rate  # Use sample rate from request
                        )
                        
                        if tts_result["success"]:
                            audio_response = tts_result["audio_data"]  # base64 encoded audio
                            VOICE_LOGGER.info(f"Text-to-speech conversion successful, audio size: {len(audio_response) if audio_response else 0} chars")
                        else:
                            VOICE_LOGGER.error(f"TTS failed: {tts_result['error']}")
                            audio_response = ""  # Ensure audio_response is empty string on failure
                    except Exception as e:
                        VOICE_LOGGER.error(f"Error in text-to-speech conversion: {e}")
                        audio_response = ""  # Ensure audio_response is empty string on exception
                else:
                    VOICE_LOGGER.warning("AliVoice client not available for text-to-speech conversion")
                    # Even if AliVoice is not available, we still return empty audio_response field
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                
                # Always include both response and audio_response fields
                response = {
                    "response": response_content, 
                    "model": model_config_name,
                    "audio_response": audio_response or ""  # Return empty string if no audio
                }
                
                # Log the full response to web_chat.log, but simplify audio data to avoid long base64 strings
                log_response = response.copy()
                if 'audio_response' in log_response and log_response['audio_response']:
                    log_response['audio_response'] = 'not null'  # Replace long base64 string with 'not null'
                VOICE_LOGGER.info(f"Chat response: {json.dumps(log_response, ensure_ascii=False)}")
                
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                
            except Exception as e:
                import traceback
                error_msg = f"Error generating response: {str(e)}"
                VOICE_LOGGER.error(error_msg)
                VOICE_LOGGER.error(f"Full traceback: {traceback.format_exc()}")
                
                # Log detailed information about the error context
                VOICE_LOGGER.error(f"Error context - Model: {model_config_name}, Character: {character_name}, User message: '{user_message[:100]}...', Input token count: {input_token_count if 'input_token_count' in locals() else 'N/A'}, Output token count: {output_token_count if 'output_token_count' in locals() else 'N/A'}")
                
                self.send_response(500)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                
                # Always return consistent response format with response and audio_response fields
                response = {
                    "response": "", 
                    "audio_response": "",
                    "error": str(e)
                }
                # Log the error response to web_chat.log, but simplify audio data to avoid long base64 strings
                log_response = response.copy()
                if 'audio_response' in log_response and log_response['audio_response']:
                    log_response['audio_response'] = 'not null'  # Replace long base64 string with 'not null'
                VOICE_LOGGER.error(f"Chat error response: {json.dumps(log_response, ensure_ascii=False)}")
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                
        elif parsed_path.path == '/speech_to_text':
            # Handle speech-to-text conversion
            try:
                content_type = self.headers.get('Content-Type', '')
                
                if content_type.startswith('audio/'):
                    # Handle raw audio data as byte stream
                    content_length = int(self.headers['Content-Length'])
                    audio_bytes = self.rfile.read(content_length)
                    
                    # Format and sample_rate can be passed via query parameters
                    parsed_query = parse_qs(urlparse(self.path).query)
                    audio_format = parsed_query.get('format', ['wav'])[0]
                    sample_rate = int(parsed_query.get('sample_rate', [16000])[0])
                else:
                    # Handle JSON data
                    request_data = json.loads(post_data)
                    audio_data = request_data.get('audio', '')  # base64 encoded audio data
                    audio_format = request_data.get('format', 'wav')
                    sample_rate = request_data.get('sample_rate', 16000)
                    
                    # If audio_data is a base64 string, decode it to bytes
                    if isinstance(audio_data, str):
                        audio_bytes = base64.b64decode(audio_data)
                    else:
                        audio_bytes = audio_data
                
                # Perform speech-to-text conversion if AliVoice client is available
                if ALI_VOICE_CLIENT:
                    try:
                        VOICE_LOGGER.info(f"Starting speech-to-text conversion, format: {audio_format}, sample_rate: {sample_rate}, audio size: {len(audio_bytes)} bytes")
                        asr_result = ALI_VOICE_CLIENT.speech_to_text(
                            audio_data=audio_bytes,
                            format=audio_format,
                            sample_rate=sample_rate
                        )
                        
                        if asr_result["success"]:
                            VOICE_LOGGER.info(f"Speech-to-text conversion successful: '{asr_result['text']}'")
                            response = {
                                "success": True,
                                "text": asr_result["text"]
                            }
                        else:
                            VOICE_LOGGER.error(f"ASR failed: {asr_result['error']}")
                            response = {
                                "success": False,
                                "error": asr_result["error"]
                            }
                    except Exception as e:
                        VOICE_LOGGER.error(f"Error in speech-to-text conversion: {e}")
                        response = {
                            "success": False,
                            "error": str(e)
                        }
                else:
                    VOICE_LOGGER.error("AliVoice client not available for speech-to-text conversion")
                    response = {
                        "success": False,
                        "error": "AliVoice client not available"
                    }
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                
            except json.JSONDecodeError:
                self.send_response(400)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                response = {"error": "Invalid JSON"}
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                return
            except Exception as e:
                VOICE_LOGGER.error(f"Error in speech-to-text request: {e}")
                self.send_response(500)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                response = {"error": str(e)}
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                return
                
        elif parsed_path.path == '/text_to_speech':
            # Handle text-to-speech conversion
            try:
                # Handle JSON data
                request_data = json.loads(post_data)
                text = request_data.get('text', '')
                voice = request_data.get('voice', 'aitong')
                audio_format = request_data.get('format', 'wav')
                sample_rate = request_data.get('sample_rate', 16000)
                

                
                # Perform text-to-speech conversion if AliVoice client is available
                if ALI_VOICE_CLIENT:
                    try:
                        VOICE_LOGGER.info(f"Starting text-to-speech conversion for text: '{text[:50]}...', voice: {voice}")
                        tts_result = ALI_VOICE_CLIENT.text_to_speech(
                            text=text,
                            voice=voice,
                            format=audio_format,
                            sample_rate=sample_rate
                        )
                        
                        if tts_result["success"]:
                            VOICE_LOGGER.info(f"Text-to-speech conversion successful, audio size: {len(tts_result['audio_data']) if tts_result['audio_data'] else 0} chars")
                            response = {
                                "success": True,
                                "audio": tts_result["audio_data"]  # base64 encoded audio
                            }
                        else:
                            VOICE_LOGGER.error(f"TTS failed: {tts_result['error']}")
                            response = {
                                "success": False,
                                "error": tts_result["error"]
                            }
                    except Exception as e:
                        VOICE_LOGGER.error(f"Error in text-to-speech conversion: {e}")
                        response = {
                            "success": False,
                            "error": str(e)
                        }
                else:
                    VOICE_LOGGER.error("AliVoice client not available for text-to-speech conversion")
                    response = {
                        "success": False,
                        "error": "AliVoice client not available"
                    }
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                
            except json.JSONDecodeError:
                self.send_response(400)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                response = {"error": "Invalid JSON"}
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                return
            except Exception as e:
                VOICE_LOGGER.error(f"Error in text-to-speech request: {e}")
                self.send_response(500)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                response = {"error": str(e)}
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                return
                
        elif parsed_path.path == '/switch_model':
            try:
                request_data = json.loads(post_data)
                model_config_name = request_data.get('model_config_name')
                character_name = request_data.get('character', 'peppa_pig')  # Get character name, default to peppa_pig
            except json.JSONDecodeError:
                self.send_response(400)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                response = {"error": "Invalid JSON"}
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                return
            
            if model_config_name not in MODEL_CONFIGS:
                self.send_response(400)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                response = {"error": "Model config '{}' not found".format(model_config_name)}
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                return
            
            # Validate character name
            if character_name not in CHARACTER_PROMPTS:
                # Use the first available character as default
                character_name = list(CHARACTER_PROMPTS.keys())[0] if CHARACTER_PROMPTS else 'general'
            
            # Get the character-specific history
            history_key = self.get_character_history_key(character_name)
            if history_key not in CHAT_HISTORY:
                CHAT_HISTORY[history_key] = []
            
            # When switching model, we can either:
            # 1. Keep conversation history and just update the system prompt (better for continuity) 
            # 2. Or reset to just the system prompt (as was done before)
            # Let's implement option 1 to maintain conversation continuity
            system_prompt = get_character_prompt(character_name)
            # Create new history starting with system prompt, followed by existing conversation
            new_history = [{"role": "system", "content": system_prompt}]
            # Add all existing conversation history (excluding any previous system messages)
            for msg in CHAT_HISTORY[history_key]:
                if msg["role"] != "system":  # Don't add previous system messages
                    new_history.append(msg)
            CHAT_HISTORY[history_key] = new_history
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            
            response = {"message": "Model switched to {}".format(model_config_name), "model": model_config_name, "character": character_name}
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            
        elif parsed_path.path == '/switch_character':
            try:
                request_data = json.loads(post_data)
                character_name = request_data.get('character', 'peppa_pig')
            except json.JSONDecodeError:
                self.send_response(400)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                response = {"error": "Invalid JSON"}
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                return
            
            if character_name not in CHARACTER_PROMPTS:
                # Use the first available character as default
                character_name = list(CHARACTER_PROMPTS.keys())[0] if CHARACTER_PROMPTS else 'general'
            
            # If there's an existing conversation with the new character, we keep it
            # If not, we just set the character for the next conversation
            # No need to reset history here, as it will be specific to the character
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            
            response = {"message": "Character switched to {}".format(character_name), "character": character_name}
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            
        elif parsed_path.path == '/reset':
            # Get character name from request data, default to peppa_pig
            try:
                request_data = json.loads(post_data)
                character_name = request_data.get('character', 'peppa_pig')
            except:
                character_name = 'peppa_pig'  # Default to peppa_pig if no JSON or no character specified
            
            # Validate character name
            if character_name not in CHARACTER_PROMPTS:
                # Use the first available character as default
                character_name = list(CHARACTER_PROMPTS.keys())[0] if CHARACTER_PROMPTS else 'general'
            
            # Get the character-specific history
            history_key = self.get_character_history_key(character_name)
            if history_key not in CHAT_HISTORY:
                CHAT_HISTORY[history_key] = []
            
            CHAT_HISTORY[history_key] = []
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            
            response = {"message": "Conversation history reset for character {}".format(character_name), "character": character_name}
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
    
    def log_conversation(self, user_message, assistant_response, model_name, input_tokens=None, output_tokens=None, character_name='peppa_pig', client_id=None):
        """Log the conversation to a file"""
        try:
            # Extract the actual question from contextual input if it's in scenario format
            actual_question = user_message
            # Check if the message is in the scenario evaluator format: "context\n现在轮到你（角色名）回答：actual_question"
            if "现在轮到你（" in user_message and "）回答：" in user_message:
                # Extract the part after "现在轮到你（角色名）回答："
                actual_question = user_message.split("）回答：")[-1].strip()
            elif "现在轮到你(" in user_message and ")回答：" in user_message:  # Also handle without space
                actual_question = user_message.split(")回答：")[-1].strip()
            
            # Get client ID if not provided
            if client_id is None:
                client_id = self._get_client_identifier()
            
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            log_entry = '[{0}] Model: {1}, Character: {2}, Terminal: {3}\n'.format(timestamp, model_name, character_name, client_id)
            log_entry += 'Q: {0}\n'.format(actual_question)
            log_entry += 'A: {0}\n'.format(assistant_response)
            
            # Log token counts if available
            if input_tokens is not None and output_tokens is not None:
                total_tokens = input_tokens + output_tokens
                log_entry += 'Input tokens: {0}, Output tokens: {1}, Total tokens: {2}\n'.format(
                    input_tokens, output_tokens, total_tokens)
            
            log_entry += '-' * 50 + '\n'
            
            # Use the new logger to write to the rotating/compressed log file
            QS_LOGGER.info(log_entry.strip())  # strip to avoid double newlines
            
        except Exception as e:
            print('Error writing to log file: {0}'.format(e))

    def get_html_content(self):
        return """
<!DOCTYPE html>
<html>
<head>
    <title>虚拟伙伴聊天机器人</title>
    <meta charset="utf-8">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f9f9f9;
        }
        
        .chat-container {
            height: 60vh;
            overflow-y: auto;
            border: 1px solid #ddd;
            padding: 15px;
            background-color: white;
            border-radius: 8px;
            margin-bottom: 15px;
        }
        
        .message {
            margin-bottom: 10px;
            padding: 10px;
            border-radius: 8px;
            max-width: 80%;
        }
        
        .user-message {
            background-color: #e3f2fd;
            margin-left: auto;
        }
        
        .assistant-message {
            background-color: #f1f8e9;
            margin-right: auto;
        }
        
        .system-message {
            background-color: #fff3e0;
            text-align: center;
            font-style: italic;
        }
        
        .input-container {
            display: flex;
            gap: 10px;
        }
        
        #message-input {
            flex: 1;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        
        button {
            padding: 10px 15px;
            background-color: #4caf50;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        
        button:hover {
            background-color: #45a049;
        }
        
        .controls {
            margin-bottom: 15px;
            display: flex;
            gap: 10px;
            align-items: center;
            flex-wrap: wrap;
        }
        
        select {
            padding: 8px;
            border-radius: 4px;
            border: 1px solid #ddd;
        }
        
        .typing-indicator {
            color: #999;
            font-style: italic;
            padding: 10px;
        }
    </style>
</head>
<body>
    <h1>🤖 虚拟伙伴聊天机器人</h1>
    <p>欢迎来和我聊天！我是一个虚拟伙伴，可以扮演不同的角色和你对话！</p>
    
    <div class="controls">
        <label for="character-select">选择角色:</label>
        <select id="character-select">
            <!-- Options will be populated by JavaScript -->
        </select>
        <label for="model-select">选择模型:</label>
        <select id="model-select">
            <!-- Options will be populated by JavaScript -->
        </select>
        <button id="switch-character-btn">切换角色</button>
        <button id="switch-model-btn">切换模型</button>
        <button id="reset-btn">重置对话</button>
    </div>
    
    <div id="chat-container" class="chat-container"></div>
    
    <div class="input-container">
        <input type="text" id="message-input" placeholder="输入你的消息..." />
        <button id="send-btn">发送</button>
    </div>
    
    <div id="typing-indicator" class="typing-indicator" style="display: none;">角色正在思考中...</div>

    <script>
        // DOM elements
        const chatContainer = document.getElementById('chat-container');
        const messageInput = document.getElementById('message-input');
        const sendBtn = document.getElementById('send-btn');
        const modelSelect = document.getElementById('model-select');
        const characterSelect = document.getElementById('character-select');
        const switchCharacterBtn = document.getElementById('switch-character-btn');
        const switchModelBtn = document.getElementById('switch-model-btn');
        const resetBtn = document.getElementById('reset-btn');
        const typingIndicator = document.getElementById('typing-indicator');
        
        let currentModel = 'qwen3-8B';
        let currentCharacter = 'peppa_pig'; // Default to Peppa Pig
        let currentCharacterDisplay = '小猪佩奇'; // Default display name
        
        // Function to update the character display name based on selected character
        function getCharacterDisplayName(characterName) {
            const characterNames = {
                'peppa_pig': '小猪佩奇',
                'nezha': '哪吒',
                'general': '虚拟伙伴'
            };
            return characterNames[characterName] || characterName;
        }
        
        // Function to add a message to the chat container
        function addMessage(role, content) {
            const messageDiv = document.createElement('div');
            messageDiv.classList.add('message');
            
            if (role === 'user') {
                messageDiv.classList.add('user-message');
                messageDiv.textContent = '小朋友: ' + content;
            } else if (role === 'assistant') {
                messageDiv.classList.add('assistant-message');
                const displayName = getCharacterDisplayName(currentCharacter);
                messageDiv.textContent = displayName + ': ' + content;
            } else if (role === 'system') {
                messageDiv.classList.add('system-message');
                messageDiv.textContent = content;
            }
            
            chatContainer.appendChild(messageDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
        
        // Function to get available characters
        async function loadCharacters() {
            try {
                const response = await fetch('/characters');
                const data = await response.json();
                
                // Clear existing options
                characterSelect.innerHTML = '';
                
                // Add new options
                data.characters.forEach(character => {
                    const option = document.createElement('option');
                    option.value = character;
                    option.textContent = getCharacterDisplayName(character);
                    if (character === currentCharacter) {
                        option.selected = true;
                    }
                    characterSelect.appendChild(option);
                });
            } catch (error) {
                console.error('Error loading characters:', error);
            }
        }
        
        // Function to get available models
        async function loadModels() {
            try {
                const response = await fetch('/models');
                const data = await response.json();
                
                // Clear existing options
                modelSelect.innerHTML = '';
                
                // Add new options
                data.models.forEach(model => {
                    const option = document.createElement('option');
                    option.value = model;
                    option.textContent = model;
                    if (model === currentModel) {
                        option.selected = true;
                    }
                    modelSelect.appendChild(option);
                });
            } catch (error) {
                console.error('Error loading models:', error);
            }
        }
        
        // Function to send a message
        async function sendMessage() {
            const message = messageInput.value.trim();
            if (!message) return;
            
            // Add user message to chat
            addMessage('user', message);
            messageInput.value = '';
            
            // Show typing indicator
            typingIndicator.style.display = 'block';
            
            try {
                // Send message to backend
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        message: message,
                        model_config_name: currentModel,
                        character: currentCharacter
                    })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    // Add assistant response to chat
                    addMessage('assistant', data.response);
                    currentModel = data.model;
                    currentCharacter = data.character || currentCharacter; // Update character if provided
                    
                    // Update model selection to reflect current model
                    if (modelSelect.value !== currentModel) {
                        const option = Array.from(modelSelect.options).find(opt => opt.value === currentModel);
                        if (option) option.selected = true;
                    }
                    
                    // Update character selection to reflect current character
                    if (characterSelect.value !== currentCharacter) {
                        const option = Array.from(characterSelect.options).find(opt => opt.value === currentCharacter);
                        if (option) option.selected = true;
                    }
                } else {
                    addMessage('system', '错误: ' + data.error);
                }
            } catch (error) {
                addMessage('system', '错误: ' + error.message);
            } finally {
                // Hide typing indicator
                typingIndicator.style.display = 'none';
            }
        }
        
        // Function to switch character
        async function switchCharacter() {
            const newCharacter = characterSelect.value;
            
            if (newCharacter !== currentCharacter) {
                try {
                    const response = await fetch('/switch_character', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            character: newCharacter
                        })
                    });
                    
                    const data = await response.json();
                    
                    if (response.ok) {
                        currentCharacter = data.character;
                        addMessage('system', data.message);
                        updateOpeningMessage(currentCharacter);
                    } else {
                        addMessage('system', '错误: ' + data.error);
                    }
                } catch (error) {
                    addMessage('system', '错误: ' + error.message);
                }
            }
        }
        
        // Function to switch model
        async function switchModel() {
            const newModel = modelSelect.value;
            
            if (newModel !== currentModel) {
                try {
                    const response = await fetch('/switch_model', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            model_config_name: newModel,
                            character: currentCharacter
                        })
                    });
                    
                    const data = await response.json();
                    
                    if (response.ok) {
                        currentModel = data.model;
                        currentCharacter = data.character || currentCharacter; // Update character if provided
                        addMessage('system', data.message);
                        // Update opening message only if character actually changed
                        if (data.character && data.character !== currentCharacter) {
                            updateOpeningMessage(data.character);
                        }
                    } else {
                        addMessage('system', '错误: ' + data.error);
                    }
                } catch (error) {
                    addMessage('system', '错误: ' + error.message);
                }
            }
        }
        
        // Function to reset conversation
        async function resetConversation() {
            try {
                const response = await fetch('/reset', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        character: currentCharacter
                    })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    // Clear chat container
                    chatContainer.innerHTML = '';
                    addMessage('system', data.message);
                } else {
                    addMessage('system', '错误: ' + data.error);
                }
            } catch (error) {
                addMessage('system', '错误: ' + error.message);
            }
        }
        
        // Event listeners
        sendBtn.addEventListener('click', sendMessage);
        messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
        
        switchCharacterBtn.addEventListener('click', switchCharacter);
        switchModelBtn.addEventListener('click', switchModel);
        resetBtn.addEventListener('click', resetConversation);
        
        // Initial setup
        loadCharacters();
        loadModels();
        // Show a default message while we load the character-specific opening
        const defaultOpening = '你好！我是' + getCharacterDisplayName(currentCharacter) + '！欢迎来和我聊天！';
        addMessage('system', defaultOpening);
        
        // Load and display character-specific opening message
        loadOpeningMessage(currentCharacter, defaultOpening);
        
        addMessage('system', '你可以随时和我分享你的故事，或者问我任何问题！使用上面的下拉菜单可以切换角色哦！');
    </script>
    
    <script>
        // Function to load character-specific opening message
        async function loadOpeningMessage(character, defaultOpening) {
            try {
                const response = await fetch(`/opening?character=${character}`);
                const data = await response.json();
                
                if (data.opening) {
                    // Remove the default opening message and add the character-specific one
                    const chatContainer = document.getElementById('chat-container');
                    const messages = Array.from(chatContainer.querySelectorAll('.message.system-message'));
                    
                    // Find and remove the default opening message
                    for (let i = messages.length - 1; i >= 0; i--) {
                        const msg = messages[i];
                        const content = msg.textContent;
                        if (content === defaultOpening) {
                            msg.remove();
                            break;
                        }
                    }
                    
                    // Add the character-specific opening message
                    addMessage('system', data.opening);
                }
            } catch (error) {
                console.error('Error loading opening message:', error);
                // Keep the default message if loading fails
            }
        }
        
        // Update opening message when character is switched
        function updateOpeningMessage(newCharacter) {
            // Add a default opening message while we load the new character's opening
            const defaultOpening = '你好！我是' + getCharacterDisplayName(newCharacter) + '！欢迎来和我聊天！';
            
            // Load new opening message for the switched character
            loadOpeningMessage(newCharacter, defaultOpening);
        }
    </script>
</body>
</html>
"""

def run_server():
    global MODEL_CONFIGS, CHAT_HISTORY, ALI_VOICE_CLIENT, CHARACTER_PROMPTS, _CONTEXT_LIST
    
    # Load all character prompts
    load_character_prompts()
    
    # Load character opening messages
    load_character_opening_messages()
    
    # Load context data
    try:
        _CONTEXT_LIST = load_contexts()
        print(f"Loaded {_CONTEXT_LIST and len(_CONTEXT_LIST) or 0} context scenarios")
    except Exception as e:
        print(f"Failed to load context data: {e}")
        _CONTEXT_LIST = []
    
    # Load model configurations
    config_path = os.path.join(current_dir, "../../model_configs.json")
    model_configs = load_model_config(config_path)
    MODEL_CONFIGS = model_configs
    
    # Initialize AliVoice client if available
    if ALI_VOICE_AVAILABLE and AliVoiceClient:
        # Load voice config from model_configs.json - check if there's a voice_config object in the original configs
        # First, reload the configs as a raw list to find any voice_config object
        with open(config_path, 'r', encoding='utf-8') as f:
            raw_configs = json.load(f)
        
        # If it's a single config object, convert to list
        if isinstance(raw_configs, dict):
            raw_configs = [raw_configs]
        
        # Look for voice_config in the list of configs
        voice_config = {}
        for config in raw_configs:
            if 'voice_config' in config:
                voice_config = config['voice_config']
                break
        
        # Fallback to model_configs dict level if voice_config is still empty
        if not voice_config:
            # If voice_config was at the top level of one of the objects
            for config_name, config_data in model_configs.items():
                if 'voice_config' in config_data:
                    voice_config = config_data['voice_config']
                    break
        
        appkey = voice_config.get('appkey', os.getenv('ALI_VOICE_APPKEY', ''))
        access_key_id = voice_config.get('access_key_id', os.getenv('ALI_VOICE_ACCESS_KEY_ID', ''))
        access_key_secret = voice_config.get('access_key_secret', os.getenv('ALI_VOICE_ACCESS_KEY_SECRET', ''))
        
        if appkey and access_key_id and access_key_secret:
            try:
                ALI_VOICE_CLIENT = AliVoiceClient(appkey, access_key_id, access_key_secret)
                VOICE_LOGGER.info("AliVoice client initialized successfully")
            except Exception as e:
                VOICE_LOGGER.error(f"Failed to initialize AliVoice client: {e}")
                ALI_VOICE_CLIENT = None
        else:
            VOICE_LOGGER.warning("AliVoice configuration not found, skipping initialization")
    else:
        VOICE_LOGGER.warning("AliVoice module not available")
    
    # Initialize history for each character
    for character_name in CHARACTER_PROMPTS.keys():
        history_key = f"history_{character_name}"
        if history_key not in CHAT_HISTORY:
            CHAT_HISTORY[history_key] = [{"role": "system", "content": CHARACTER_PROMPTS[character_name]}]
    
    # Start the server
    server_address = ('', 3000)
    httpd = HTTPServer(server_address, GeneralChatHandler)
    print("Starting server on http://localhost:3000")
    print("Available characters:", list(CHARACTER_PROMPTS.keys()))
    print("Press Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        # Close the logging handlers to properly compress and save the current log files
        for handler in logging.root.handlers[:]:
            if isinstance(handler, RotatingCompressedLogHandler):
                handler.close()
        # Also close the QS_HANDLER if it exists
        if 'QS_HANDLER' in globals():
            QS_HANDLER.close()
        if 'VOICE_HANDLER' in globals():
            VOICE_HANDLER.close()
        httpd.shutdown()
        print("Server stopped.")

if __name__ == "__main__":
    run_server()