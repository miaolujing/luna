# Luna 项目说明

本项目包含多个Python脚本，用于生成儿童对话测试用例、运行测试、评估模型响应以及提供多角色风格的Web聊天界面。

## 项目架构

### 1. 通用服务层 (service/)
- **general_chat_service.py**: 通用聊天服务主入口，支持多角色切换、情境感知和日志记录
- **peppa_pig_character.py**: 小猪佩奇角色实现
- **nezha_character.py**: 哪吒角色实现  
- **general_character.py**: 通用角色实现
- **ali_voice.py**: 阿里云语音服务封装

### 2. 评估模块 (evaluate/)
- **peppa_pig_scenario_evaluator.py**: 从真实佩奇对话中提取场景进行评估
- **peppa_pig_structured_evaluator.py**: 结构化评估佩奇对话表现
- **convert_peppa_script_to_test_cases.py**: 将佩奇对话脚本转换为测试场景

## 脚本功能说明

### 1. service/general_chat_service.py
**功能：** 提供多角色风格的Web聊天界面
- **用途：** 创建一个Web应用，支持多个虚拟角色与用户进行对话
- **特点：** 
  - 基于HTTP服务器的Web界面
  - 支持多个角色（小猪佩奇、哪吒、通用角色等）
  - 支持切换不同模型进行对话
  - 支持角色切换功能
  - 具备情境感知能力，可以根据用户输入自动匹配相关情境并调整角色回应
  - 终端独立对话历史：每个终端（客户端）拥有独立的对话历史记录，通过X-Client-ID或X-Session-ID请求头或IP地址进行区分
  - 记录对话历史和日志，包括终端ID信息
  - 统计每次调用的输入、输出和总token数量
  - 在日志中输出实际发送给大模型的提示词，便于调试和分析
- **使用方法：**
  ```bash
  python -m src.main
  ```
  或
  ```bash
  cd src && python main.py
  ```
  然后在浏览器中访问 `http://localhost:3000`

### 2. service/peppa_pig_character.py
**功能：** 小猪佩奇角色提示词和行为定义
- **用途：** 定义小猪佩奇的性格特点、说话方式和行为模式
- **特点：**
  - 基于4岁儿童心理学的详细角色设定
  - 包含12个关键行为模式参考
  - 强调使用第一人称的对话方式
- **使用方法：** 由general_chat_service.py自动加载

### 3. service/nezha_character.py
**功能：** 哪吒角色提示词和行为定义
- **用途：** 定义哪吒的性格特点、说话方式和行为模式
- **特点：**
  - 基于神话人物哪吒的性格特征
  - 包含勇敢、正义、孝顺等特质
  - 强调使用第一人称的对话方式
- **使用方法：** 由general_chat_service.py自动加载

### 4. service/general_character.py
**功能：** 通用角色提示词和行为定义  
- **用途：** 定义一个友好的通用虚拟伙伴角色
- **特点：**
  - 友好、聪明、乐于助人的角色设定
  - 适合一般性对话用途
  - 强调使用第一人称的对话方式
- **使用方法：** 由general_chat_service.py自动加载

### 5. evaluate/peppa_pig_scenario_evaluator.py
**功能：** 从真实佩奇对话中提取场景进行评估
- **用途：** 从真实的佩奇剧集对话脚本中提取测试场景，模拟完整对话流程，评估AI模型在不同场景下模仿佩奇行为和语言风格的表现
- **特点：**
  - 从真实佩奇剧集中提取场景
  - 模拟完整的对话流程
  - 评估模型在场景中的表现
  - 支持多模型对比测试
- **使用方法：**
  ```bash
  python -m src.evaluate.peppa_pig_scenario_evaluator
  ```
  或离线分析模式：
  ```bash
  python -m src.evaluate.peppa_pig_scenario_evaluator --analyze
  ```

### 6. evaluate/peppa_pig_structured_evaluator.py
**功能：** 结构化评估佩奇对话表现
- **用途：** 从结构化的JSON测试用例中加载场景，评估模型对佩奇角色的模仿程度
- **特点：**
  - 从JSON文件加载结构化测试用例
  - 按场景分组进行测试
  - 使用多种评估指标
  - 生成CSV格式的人工标注文件
- **使用方法：**
  ```bash
  python -m src.evaluate.peppa_pig_structured_evaluator
  ```

### 7. evaluate/convert_peppa_script_to_test_cases.py
**功能：** 将佩奇对话脚本转换为测试场景
- **用途：** 将佩奇剧集对话脚本转换为可用于评估的测试场景格式
- **特点：**
  - 解析佩奇剧集对话脚本
  - 提取对话场景
  - 转换为结构化的测试用例格式
- **使用方法：**
  ```bash
  python -m src.evaluate.convert_peppa_script_to_test_cases
  ```

## Multi-Character Web Chat API 接口说明

### 1. GET / - Web界面
- **方法**: GET
- **URL**: `/`
- **描述**: 返回主Web聊天界面的HTML页面
- **参数**: 无
- **响应**: HTML内容

### 2. GET /models - 获取可用模型
- **方法**: GET
- **URL**: `/models`
- **描述**: 返回可用的模型配置列表
- **参数**: 无
- **响应格式**:
```json
{
  "models": ["model_name_1", "model_name_2", "..."]
}
```

### 3. GET /characters - 获取可用角色
- **方法**: GET
- **URL**: `/characters`
- **描述**: 返回可用的角色列表
- **参数**: 无
- **响应格式**:
```json
{
  "characters": ["peppa_pig", "nezha", "general", "..."]
}
```

### 4. GET /history - 获取对话历史
- **方法**: GET
- **URL**: `/history?character={character_name}`
- **描述**: 返回指定角色的对话历史记录
- **参数**:
  - `character` (可选): 角色名称，默认为第一个可用角色
- **响应格式**:
```json
{
  "history": [
    {"role": "user/system/assistant", "content": "消息内容"},
    ...
  ]
}
```

### 5. GET /openings - 获取所有角色开场白
- **方法**: GET
- **URL**: `/openings`
- **描述**: 返回所有角色的开场白消息
- **参数**: 无
- **响应格式**:
```json
{
  "openings": {
    "peppa_pig": "角色对应的开场白消息",
    "nezha": "角色对应的开场白消息", 
    "general": "角色对应的开场白消息"
  }
}
```

### 6. GET /opening - 获取指定角色开场白
- **方法**: GET
- **URL**: `/opening?character={character_name}`
- **描述**: 返回指定角色的开场白消息
- **参数**:
  - `character` (可选): 角色名称，默认为第一个可用角色
- **响应格式**:
```json
{
  "opening": "角色对应的开场白消息",
  "character": "角色名称"
}
```

### 7. POST /chat - 聊天消息
- **方法**: POST
- **URL**: `/chat`
- **描述**: 发送聊天消息并获取指定角色的回复，支持文本输入和语音输入。每个终端（客户端）拥有独立的对话历史，历史记录限制为3000字符。
- **Content-Type**:
  - `application/json` (文本消息或base64音频消息)
  - `audio/*` (原始音频字节流，如: audio/wav, audio/mp3, audio/mpeg, audio/amr)

**请求参数 (application/json 格式)**:
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| message | string | 否 | 用户输入的文本消息 |
| audio | string | 否 | base64编码的音频数据（用于语音输入） |
| model_config_name | string | 否 | 模型配置名称，默认为'qwen3-8B' |
| character | string | 否 | 角色名称，默认为'peppa_pig' ,支持'nezha'，'general'|
| custom_prompt | string | 否 | 自定义系统提示词 |
| voice | string | 否 | TTS语音类型，默认为'aitong'，接受任意语音参数，具体支持的语音以阿里云服务为准 |
| tts_format | string | 否 | TTS音频格式，默认为'wav' |
| tts_sample_rate | number | 否 | TTS采样率，默认为16000 |
| asr_format | string | 否 | ASR音频格式，默认为'wav' |
| asr_sample_rate | number | 否 | ASR采样率，默认为16000 |

**请求参数 (audio/* 格式)**:
当Content-Type以`audio/`开头时，请求体直接为音频字节流，系统默认使用'peppa_pig'角色。

**请求头 (可选)**:
| 请求头 | 说明 |
|--------|------|
| X-Client-ID | 客户端唯一标识符，用于区分不同终端。如果未提供，系统将基于客户端IP地址生成标识符 |
| X-Session-ID | 会话唯一标识符，与X-Client-ID功能相同，可任选其一使用 |

**响应格式**:
```json
{
  "response": "AI模型生成的文本响应内容",
  "model": "使用的模型配置名称",
  "character": "使用的角色名称",
  "audio_response": "base64编码的语音响应（如果语音服务可用）"
}
```

**错误响应**:
```json
{
  "error": "错误描述信息"
}
```

**请求示例1 (文本消息)**:
```json
{
  "message": "你好，佩奇！",
  "model_config_name": "qwen3-8B",
  "character": "peppa_pig"
}
```

**请求示例2 (带客户端标识)**:
```json
{
  "message": "你好，佩奇！",
  "model_config_name": "qwen3-8B",
  "character": "peppa_pig"
}
```
请求头: X-Client-ID: mobile_app_user_123

**请求示例3 (带TTS参数)**:
```json
{
  "message": "你好，佩奇！",
  "model_config_name": "qwen3-8B",
  "character": "peppa_pig",
  "voice": "xiaoyun",
  "tts_format": "mp3",
  "tts_sample_rate": 8000
}
```

**请求示例4 (带ASR参数)**:
```json
{
  "audio": "base64_encoded_audio_string_here",
  "model_config_name": "qwen3-8B",
  "character": "nezha",
  "asr_format": "wav",
  "asr_sample_rate": 16000
}
```

**请求示例5 (语音输入base64)**:
```json
{
  "audio": "base64_encoded_audio_string_here",
  "model_config_name": "qwen3-8B",
  "character": "nezha"
}
```

**请求示例6 (直接音频流)**:
直接发送音频字节流数据 (Content-Type: audio/wav)

**响应示例**:
```json
{
  "response": "你好！我是小猪佩奇！",
  "model": "qwen3-8B",
  "character": "peppa_pig",
  "audio_response": "base64_encoded_audio_response_here"
}
```

**特点**:
- 支持文本消息和语音消息输入
- 当提供音频数据时，系统会先将其转换为文本，再进行对话处理
- 音频响应功能需要阿里云语音服务正常配置和可用
- **终端独立对话历史**: 每个终端（客户端）拥有独立的对话历史记录，通过X-Client-ID或X-Session-ID请求头或IP地址进行区分
- **历史记录限制**: 每个终端的对话历史限制为3000字符，超过限制时自动截断最旧的消息
- 当对话历史过长时，系统会自动截断以保持性能

### 8. POST /switch_character - 切换角色
- **方法**: POST
- **URL**: `/switch_character`
- **描述**: 切换当前活动的角色
- **请求参数**:
```json
{
  "character": "目标角色名称"
}
```
- **响应格式**:
```json
{
  "message": "角色已切换为 {character_name}",
  "character": "角色名称"
}
```

### 9. POST /switch_model - 切换模型
- **方法**: POST
- **URL**: `/switch_model`
- **描述**: 切换当前活动的模型配置，同时可指定角色
- **请求参数**:
```json
{
  "model_config_name": "目标模型配置名称",
  "character": "角色名称（可选，默认为当前角色）"
}
```
- **响应格式**:
```json
{
  "message": "模型已切换为 {model_name}",
  "model": "模型配置名称",
  "character": "角色名称"
}
```

### 10. POST /speech_to_text - 语音转文字
- **方法**: POST
- **URL**: `/speech_to_text`
- **描述**: 将语音数据转换为文字
- **Content-Type**:
  - `application/json` (base64音频数据)
  - `audio/*` (原始音频字节流，如: audio/wav, audio/mp3等)
- **请求参数 (application/json 格式)**:
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| audio | string | 是 | base64编码的音频数据 |
| format | string | 否 | 音频格式，默认为'wav' |
| sample_rate | number | 否 | 采样率，默认为16000 |

- **请求参数 (audio/* 格式)**:
当Content-Type以`audio/`开头时，请求体直接为音频字节流，可通过查询参数传递format和sample_rate：
  - `?format=wav` - 音频格式
  - `?sample_rate=16000` - 采样率

- **成功响应格式**:
```json
{
  "success": true,
  "text": "识别出的文字内容"
}
```

- **失败响应格式**:
```json
{
  "success": false,
  "error": "错误信息"
}
```

### 11. POST /text_to_speech - 文字转语音
- **方法**: POST
- **URL**: `/text_to_speech`
- **描述**: 将文字转换为语音
- **Content-Type**: `application/json`
- **请求参数**:
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| text | string | 是 | 要转换的文字内容 |
| voice | string | 否 | 语音类型，默认为'xiaoyun' |
| format | string | 否 | 音频格式，默认为'wav' |
| sample_rate | number | 否 | 采样率，默认为16000 |

- **成功响应格式**:
```json
{
  "success": true,
  "audio": "base64编码的音频数据"
}
```

- **失败响应格式**:
```json
{
  "success": false,
  "error": "错误信息"
}
```

### 12. POST /reset - 重置对话
- **方法**: POST
- **URL**: `/reset`
- **描述**: 重置指定角色的对话历史记录
- **请求参数**:
```json
{
  "character": "角色名称（可选，默认为'peppa_pig'）"
}
```
- **响应格式**:
```json
{
  "message": "对话历史已重置 for character {character_name}",
  "character": "角色名称"
}
```

## 项目流程

1. 运行`generate_test_cases.py`生成测试用例
2. 启动`general_chat_service.py`服务（多角色支持）
3. 运行`run_test_cases.py`使用不同模型进行对话测试
4. 使用`evaluate_peppa_pig_responses.py`评估模型表现

## 配置文件

- `model_configs.json`: 包含模型配置信息，用于Web聊天和测试脚本
- `result/` 目录：存放测试用例、测试结果和评估报告

## 扩展角色

项目采用模块化设计，可以轻松扩展新角色：
1. 创建新的角色模块（如 `new_character.py`）
2. 定义该角色的提示词生成函数
3. 在 `general_chat_service.py` 中导入并注册新角色
4. 角色将在接口中自动可用

### 7. 情境感知功能

项目支持情境感知功能，能够根据用户输入自动匹配相关情境：
- **数据源：** 使用 `child_contexts.json` 文件中的情境配置
- **匹配算法：** 基于关键词匹配的算法，支持年龄范围过滤
- **应用方式：** 在用户输入前动态插入情境前缀，使角色回应更贴合实际情境
- **日志记录：** 将实际发送给大模型的系统提示词记录到日志中，便于调试和分析

## 注意事项

- 确保在执行脚本前已安装所需的依赖库
- `general_chat_service.py`需要网络连接以调用AI模型API
- 运行测试脚本前需要先启动Web聊天服务
- 多角色功能需要确保角色定义模块正确加载
- 情境感知功能需要 `child_contexts.json` 文件存在并包含有效配置
- 日志文件保存在 `result/logs/` 目录中，包含：
  - `web_chat.log`: 存放完整的Web聊天日志，包含实际发送给大模型的提示词
  - `qs.txt`: 存放对话问答日志，现在包含终端ID信息，格式为：`[时间] Model: 模型名, Character: 角色名, Terminal: 终端ID`