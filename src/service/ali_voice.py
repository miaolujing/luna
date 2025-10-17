"""
阿里云语音服务 - 核心接口
提供文字转语音(TTS)和语音转文字(ASR)功能
"""

import base64
import uuid
import time
import hmac
import hashlib
import requests
from urllib.parse import quote
from typing import Dict, Any, Optional


class AliVoiceClient:
    """阿里云语音服务客户端"""
    
    def __init__(self, appkey: str, access_key_id: str, access_key_secret: str):
        """
        初始化客户端
        
        Args:
            appkey: 阿里云AppKey
            access_key_id: AccessKey ID
            access_key_secret: AccessKey Secret
        """
        self.appkey = appkey
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.region = "cn-shanghai"
        
        self.token = None
        self.token_expire_time = 0
        
        # API地址
        self.token_url = f"https://nls-meta.{self.region}.aliyuncs.com/pop/2018-05-18/tokens"
        self.tts_url = f"https://nls-gateway.{self.region}.aliyuncs.com/stream/v1/tts"
        self.asr_url = f"https://nls-gateway.{self.region}.aliyuncs.com/stream/v1/asr"
        
        # 自动获取token
        self._refresh_token()
    
    def _get_signature(self, params: Dict[str, str]) -> str:
        """生成API签名"""
        sorted_params = sorted(params.items())
        query_string = "&".join([f"{k}={quote(str(v), safe='')}" for k, v in sorted_params])
        string_to_sign = f"GET&%2F&{quote(query_string, safe='')}"
        h = hmac.new(
            (self.access_key_secret + "&").encode('utf-8'),
            string_to_sign.encode('utf-8'),
            hashlib.sha1
        )
        return base64.b64encode(h.digest()).decode('utf-8')
    
    def _refresh_token(self) -> bool:
        """刷新Token"""
        try:
            if self.token and time.time() < self.token_expire_time - 600:
                return True
            
            params = {
                "AccessKeyId": self.access_key_id,
                "Action": "CreateToken",
                "Version": "2019-02-28",
                "Timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "Format": "JSON",
                "RegionId": self.region,
                "SignatureMethod": "HMAC-SHA1",
                "SignatureVersion": "1.0",
                "SignatureNonce": str(uuid.uuid4()),
            }
            params["Signature"] = self._get_signature(params)
            
            response = requests.get(self.token_url, params=params, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if 'Token' in result and 'Id' in result['Token']:
                    self.token = result['Token']['Id']
                    self.token_expire_time = time.time() + 24 * 3600
                    return True
            
            raise Exception(f"获取Token失败: {response.text}")
        except Exception as e:
            raise Exception(f"Token刷新失败: {e}")
    
    def text_to_speech(
        self,
        text: str,
        voice: str = "aitong",
        format: str = "wav",
        sample_rate: int = 16000,
        return_base64: bool = True
    ) -> Dict[str, Any]:
        """
        文字转语音
        
        Args:
            text: 要合成的文本
            voice: 语音类型 (aitong/xiaogang/xiaomei/kenny等)
            format: 音频格式 (wav/mp3)
            sample_rate: 采样率 (16000/8000)
            return_base64: 是否返回base64编码
        
        Returns:
            {
                "success": bool,
                "audio_data": str/bytes,  # base64或字节
                "audio_size": int,
                "error": str  # 失败时
            }
        """
        try:
            self._refresh_token()
            
            params = {
                "appkey": self.appkey,
                "token": self.token,
                "text": text,
                "format": format,
                "sample_rate": sample_rate,
                "voice": voice,
                "volume": 50,
                "speech_rate": 0,
                "pitch_rate": 0,
            }
            
            response = requests.post(self.tts_url, params=params, timeout=60)
            
            if response.status_code == 200:
                content_type = response.headers.get('Content-Type', '')
                
                if 'audio' in content_type or 'octet-stream' in content_type:
                    audio_data = response.content
                    
                    return {
                        "success": True,
                        "audio_data": base64.b64encode(audio_data).decode('utf-8') if return_base64 else audio_data,
                        "audio_size": len(audio_data),
                        "format": format
                    }
                else:
                    try:
                        error_result = response.json()
                        error_msg = error_result.get("message", "未知错误")
                    except:
                        error_msg = response.text[:200]
                    
                    return {"success": False, "error": error_msg}
            else:
                return {"success": False, "error": f"HTTP {response.status_code}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def speech_to_text(
        self,
        audio_data: bytes,
        format: str = "pcm",
        sample_rate: int = 16000
    ) -> Dict[str, Any]:
        """
        语音转文字
        
        Args:
            audio_data: 音频字节数据
            format: 音频格式 (pcm/wav/mp3)
            sample_rate: 采样率
        
        Returns:
            {
                "success": bool,
                "text": str,  # 识别文本
                "error": str  # 失败时
            }
        """
        try:
            self._refresh_token()
            
            params = {
                "appkey": self.appkey,
                "token": self.token,
                "format": format,
                "sample_rate": sample_rate,
                "enable_punctuation_prediction": "true",
                "enable_inverse_text_normalization": "true",
            }
            
            headers = {"Content-Type": "application/octet-stream"}
            
            response = requests.post(
                self.asr_url,
                params=params,
                headers=headers,
                data=audio_data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get("status") == 20000000:
                    return {
                        "success": True,
                        "text": result.get("result", "")
                    }
                else:
                    return {
                        "success": False,
                        "error": result.get("message", "未知错误")
                    }
            else:
                return {"success": False, "error": f"HTTP {response.status_code}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

