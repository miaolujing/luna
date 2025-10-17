# Luna 项目开发规范与结构说明

## Python 编程规范

### 代码风格
- 遵循 PEP 8 编码规范
- 使用 4 个空格缩进
- 文件编码使用 UTF-8
- 行长度不超过 100 个字符
- 使用有意义的变量和函数命名

### 命名规范
- 模块名和包名使用小写字母，单词间可用下划线
- 类名使用驼峰命名法 (CamelCase)
- 函数和变量名使用小写字母，单词间用下划线分隔 (snake_case)
- 常量使用大写字母，单词间用下划线分隔

### 注释规范
- 文件头部包含编码声明和模块说明
- 函数和类使用 docstring 进行说明
- 重要逻辑和复杂代码段添加注释
- 遵循 Google Python Style Guide 的 docstring 格式

### 导入规范
- 按标准库、第三方库、本地库的顺序分组导入
- 每组导入之间用空行分隔
- 避免使用 `from module import *` 的导入方式

### 错误处理
- 合理使用异常处理机制
- 提供清晰的错误信息
- 避免忽略异常

## 项目目录结构

```
AI-TEST/
├── .gitignore                 # Git 忽略文件配置
├── model_configs.json         # 模型配置文件
├── README.md                  # 项目功能说明
├── README_project_guide.md    # 本文件 - 开发规范与结构说明
├── agentScopeDoc/            # AgentScope 相关文档
│   ├── 常见问题.md
│   ├── 创建消息.md
│   ├── 创建ReAct智能体.md
│   ├── 工具.md
│   ├── 管道 (Pipeline).md
│   ├── 核心概念.md
│   └── 记忆.md
├── psychologyKnowledgeBase/  # 心理学知识库
├── result/                   # 测试结果和输出目录
│   ├── test_cases/           # 生成的测试用例
│   ├── test_results/         # 测试结果
│   └── evaluation_report_*/  # 评估报告
├── samples/                  # 示例文件目录
└── src/                      # 源代码目录
    ├── evaluate/                           # 评估脚本目录
    │   ├── peppa_pig_scenario_evaluator.py    # 佩奇场景评测脚本
    │   ├── peppa_pig_structured_evaluator.py  # 佩奇结构化评测脚本
    │   ├── convert_peppa_script_to_test_cases.py # 脚本转换工具
    │   └── compare_evaluation.py              # 评估结果比较
    └── service/                          # 服务脚本目录
        └── peppa_pig_web_chat.py           # 小猪佩奇网页聊天
```

## 主要模块功能

- `src/`: 包含项目的核心源代码
  - `service/peppa_pig_web_chat.py`: 提供小猪佩奇风格的Web聊天界面
  - `evaluate/peppa_pig_scenario_evaluator.py`: 从真实佩奇对话中提取场景进行评估
  - `evaluate/peppa_pig_structured_evaluator.py`: 结构化评估佩奇对话表现
  - `evaluate/convert_peppa_script_to_test_cases.py`: 将佩奇对话脚本转换为测试场景
  - `evaluate/compare_evaluation.py`: 比较不同的评估结果

- `result/`: 存放项目运行生成的各类结果文件
- `agentScopeDoc/`: 包含AgentScope框架的相关文档

## 技术文档

### 核心技术栈
- Python 3.x
- Web框架 (用于聊天界面)
- OpenAI API 客户端
- JSON 数据格式

### 设计模式与架构
- Web服务: HTTP服务器模式
- 测试框架: 自动化测试流程
- 评估系统: 基于规则的评估算法

### 扩展功能与接口
- 模型配置支持
- 多模型测试能力
- 结果评估与报告生成

### [技术文档详细内容待补充]

[此处将添加更详细的技术架构、API文档、算法说明等内容]