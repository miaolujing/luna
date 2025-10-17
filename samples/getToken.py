# 请确保已经安装了DashScope Python SDK
from dashscope import get_tokenizer

# 获取tokenizer对象，目前只支持通义千问系列模型
tokenizer = get_tokenizer('qwen-turbo')

input_str = '通义千问具有强大的能力。'

# 将字符串切分成token并转换为token id
tokens = tokenizer.encode(input_str)
print(f"经过切分后的token id为：{tokens}。")
print(f"经过切分后共有{len(tokens)}个token")

# 将token id转化为字符串并打印出来
for i in range(len(tokens)):
    print(f"token id为{tokens[i]}对应的字符串为：{tokenizer.decode(tokens[i])}")
