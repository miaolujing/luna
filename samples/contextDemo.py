import json
import re
from typing import Optional, List


# 加载情境配置（建议在程序启动时加载一次）
def load_contexts(json_path: str = "child_contexts.json"):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["contexts"]


# 全局缓存（避免重复读文件）
_CONTEXT_LIST = load_contexts()


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
        str or None: 匹配到的情境指令文本，如“小朋友害怕晚上一个人睡觉”
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