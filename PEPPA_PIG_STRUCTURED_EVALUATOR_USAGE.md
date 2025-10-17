# 小猪佩奇结构化评测脚本使用说明

## 概述

`src/evaluate/peppa_pig_structured_evaluator.py` 是一个专门用于评估小猪佩奇聊天机器人性能的结构化评测脚本。该脚本从结构化的JSON测试用例文件中加载场景，评估AI模型在不同场景下模仿小猪佩奇行为和语言风格的表现。

## 功能特点

- 从结构化的JSON文件加载测试用例
- 按场景分组进行测试
- 使用多种评估指标
- 支持多模型对比测试
- 生成CSV格式的人工标注文件
- 每个场景测试结束后重置对话历史
- 生成详细的JSON报告和摘要报告

## 评分标准

脚本使用多种评估指标来衡量模型表现：

### 1. Exact Match Accuracy (完全匹配准确率)
- 检查预测响应与期望响应是否完全一致
- 返回值：0.0（完全不匹配）或 1.0（完全匹配）

### 2. Fuzzy Match (模糊匹配)
- 使用 `SequenceMatcher` 计算字符串级别的相似度
- 返回值：0.0 到 1.0（1.0 表示完全相似）

### 3. 编辑距离 (Edit Distance)
- 计算两个字符串之间的归一化编辑距离
- 返回值：0.0 到 1.0（1.0 表示完全相同）

### 4. Sentence-BERT 语义相似度
- 使用 Sentence-BERT 模型计算语义层面的相似度
- 返回值：0.0 到 1.0（1.0 表示语义完全一致）

### 5. 基于关键词的匹配度
- 使用 Jaccard 相似度计算关键词层面的匹配
- 返回值：0.0 到 1.0（1.0 表示完全匹配）

### 6. 综合评分 (Combined Score)
- 加权平均评分，权重分配如下：
  - Exact Match: 0.5
  - Fuzzy Match: 0.2
  - Edit Distance: 0.1
  - Sentence-BERT: 0.1
  - Keyword Similarity: 0.1

## 输入文件要求

脚本从 `../../result/testCase/peppa_structured_test_cases.json` 读取测试用例，文件应包含以下结构：

```json
{
  "test_cases_by_scene": {
    "场景名称": [
      {
        "context": "触发佩奇回应的上下文",
        "expected_response": "佩奇的期望回应",
        "scene": "场景名称",
        "dialogue_index": "对话索引"
      }
    ]
  }
}
```

## 输出文件

### 1. CSV文件 - 人工标注
文件路径: `../../result/peppa_structured_evaluation_[timestamp]_human_annotation.csv`

**字段含义:**
- `scene`: 场景名称
- `dialogue_index`: 对话索引
- `context`: 触发佩奇回应的上下文
- `expected_response`: 佩奇的期望回应
- `prediction`: 模型生成的实际回应
- `exact_match`: 完全匹配分数
- `content_correct`: 内容正确性（待人工填写）
- `style_consistent`: 风格一致性（待人工填写）
- `notes`: 备注（待人工填写）

### 2. JSON报告 - 详细评估结果
文件路径: `../../result/peppa_structured_evaluation_[timestamp]_report.json`

**字段含义:**
- `evaluation_info`: 评估信息对象
  - `timestamp`: 评估执行的时间戳
  - `models_evaluated`: 参与评估的模型列表
  - `total_test_cases`: 总测试用例数量
- `results`: 评估结果数组，每个结果包含：
  - `model`: 模型名称
  - `scene`: 场景名称
  - `dialogue_index`: 对话索引
  - `context`: 上下文
  - `expected_response`: 期望的佩奇回应
  - `prediction`: 模型生成的实际回应
  - `metrics`: 评估指标对象
    - `exact_match`: 完全匹配分数
    - `fuzzy_match`: 模糊匹配分数
    - `edit_distance`: 编辑距离分数
    - `sentence_bert`: Sentence-BERT分数
    - `keyword_similarity`: 关键词匹配度分数
    - `combined_score`: 综合评分

### 3. 文本摘要报告
文件路径: `../../result/peppa_structured_evaluation_[timestamp]_summary.txt`

**字段含义:**
- `Timestamp`: 评估完成的时间
- `Models evaluated`: 参与评估的模型
- `Total test cases`: 总测试用例数量
- 按模型分组的统计信息：
  - `Test cases`: 该模型处理的测试用例数量
  - `Average exact match`: 平均完全匹配分数
  - `Average fuzzy match`: 平均模糊匹配分数
  - `Average BERT similarity`: 平均BERT语义相似度

## 使用方法

### 运行评估
```bash
python -m src.evaluate.peppa_pig_structured_evaluator
```

或者在 `src/evaluate/` 目录下直接运行：
```bash
python peppa_pig_structured_evaluator.py
```

**注意：** 运行评估前需要启动小猪佩奇聊天服务器：
```bash
python -m src.service.peppa_pig_web_chat
```

### 评测流程
1. 从 `peppa_structured_test_cases.json` 加载结构化测试用例
2. 按场景分组处理测试用例
3. 将上下文发送到聊天API获得模型响应
4. 使用多种评估指标对响应进行评估
5. 每个场景测试结束后重置对话历史
6. 生成CSV、JSON和文本摘要报告

## 依赖库

- Python标准库 (json, re, time, requests, sys, os, csv, urllib.parse, difflib, datetime)
- jieba (可选，用于中文关键词提取)
- scikit-learn (可选，用于TF-IDF计算，但脚本中未直接使用)
- sentence-transformers (可选，用于Sentence-BERT计算)

如果缺少这些库，脚本会给出警告但仍可运行(使用基础功能)。

## API 接口调用

### /chat 接口
- **URL**: `http://localhost:8000/chat`
- **方法**: POST
- **Headers**: `Content-Type: application/json`
- **Body**:
```json
{
  "message": "上下文内容",
  "model_config_name": "模型名称"
}
```

### /reset 接口
- **URL**: `http://localhost:8000/reset`
- **方法**: POST
- **Headers**: `Content-Type: application/json`
- **Body**: 无

## 版本历史

### v1.0
- 初始版本发布
- 实现结构化评测功能
- 支持多指标评估
- 生成多种格式的报告