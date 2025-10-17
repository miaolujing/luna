import asyncio
import agentscope
from agentscope.agent import UserAgent, ReActAgent
from agentscope.model import OpenAIChatModel
from agentscope.formatter import DeepSeekChatFormatter
from agentscope.pipeline import sequential_pipeline
from agentscope.message import Msg
import json
import os


# 读取模型配置
def load_model_config(config_path, config_name):
    """Load model configuration from JSON file"""
    with open(config_path, 'r', encoding='utf-8') as f:
        configs = json.load(f)

    # 如果是单个配置对象，转换为列表
    if isinstance(configs, dict):
        configs = [configs]

    # 查找指定名称的配置
    for config in configs:
        if config.get('config_name') == config_name:
            return config

    raise ValueError(f"Configuration '{config_name}' not found in {config_path}")


# 初始化AgentScope
agentscope.init(
    project="ChatExample",
    name="DialogAgentExample",
    studio_url="http://192.168.99.103:3000"
)

# 加载模型配置
model_config = load_model_config("../model_configs.json", "qwen3-8B")

# 创建对话Agent（使用ReActAgent替代DialogAgent）
dialog_agent = ReActAgent(
    name="Assistant",
    sys_prompt="你是一个AI助手，你会回答用户的问题。",
    model=OpenAIChatModel(
        model_name=model_config["model_name"],
        api_key=model_config["api_key"],
        stream=True,
        client_args=model_config.get("client_args", {}),
    ),
    formatter=DeepSeekChatFormatter(),
)

# 创建用户Agent
user_agent = UserAgent(name="User")


# 开始对话 user and assistant
async def main():
    x = None
    while x is None or (isinstance(x, Msg) and x.content != "exit"):
        x = await sequential_pipeline([dialog_agent, user_agent], x)


if __name__ == "__main__":
    asyncio.run(main())