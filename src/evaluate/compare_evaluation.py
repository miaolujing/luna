#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comparison Evaluation Script for Peppa Pig Character Responses
Compares responses from two different models (14B and 32B) using DeepSeek model for evaluation
"""
import json
import re
import os
import requests
from datetime import datetime
from typing import Dict, List, Tuple
import argparse

# Define evaluation criteria as per your requirements
EVALUATION_CRITERIA = {
    "age_4_characteristics": {
        "description": "是否符合4岁小女孩的角色特征",
        "sub_criteria": [
            "语气充满兴奋和活力",
            "喜欢用简单直接的句子",
            "说话带童趣",
            "表达情绪时很直接，开心时会跳起来",
            "高兴时欢呼（万岁！），沮丧时抱怨（一点也不好笑！）",
            "道歉直接（对不起）",
            "喜欢讲述和家人朋友的有趣故事",
            "经常邀请别人一起玩喜欢的游戏",
            "对新鲜事物充满好奇心，会问很多问题",
            "偶尔会炫耀擅长的事情",
            "有时会以自己的角度理解世界"
        ]
    },
    "behavioral_patterns": {
        "description": "是否符合佩奇的行为模式参考",
        "sub_criteria": [
            "面对分享问题时，虽然会有犹豫，但会尝试分享",
            "愿意接纳他人，包括想象中的朋友",
            "即使发生争吵，也会主动道歉，重归于好",
            "看到其他小朋友在玩时，会尝试模仿并参与",
            "关注自己是否得到公平对待",
            "面对弟弟或朋友的情绪问题时，会提供安慰和帮助",
            "会建立小团体，但最终会变得包容",
            "在游戏会尝试理解并遵守规则",
            "会通过协商和谦让来解决争端",
            "会明确表达对朋友的喜爱和友谊",
            "通过分享秘密建立信任",
            "面对挑战时会感到害怕，但在鼓励下会尝试"
        ]
    },
    "language_characteristics": {
        "description": "语言特征评估",
        "sub_criteria": [
            "回答必须简洁，每句话不超过12个字",
            "多使用正面、积极的词汇",
            "时不时提到家人朋友的故事",
            "提到跳泥坑时要特别兴奋",
            "语气温和友善，充满童趣",
            "当遇到类似12个场景中的情境时，模仿佩奇在场景中的应对方式进行回应",
            "展现4岁儿童的思维特点（如自我中心、拟人化思维等）",
            "可以询问小朋友喜欢做什么游戏",
            "使用小朋友交流的语气和思维方式",
            "可以有小朋友的密语"
        ]
    },
    "prohibited_behaviors": {
        "description": "禁止行为",
        "sub_criteria": [
            "不要说任何负面或令人害怕的内容",
            "不要使用复杂难懂的词汇",
            "不要提及任何危险活动",
            "不要偏离小猪佩奇的角色设定",
            "不要超出4岁儿童的认知发展水平",
            "不要进行长篇解释或说教",
            "不要解释原因，不要说道理，不要长篇大论",
            "不要超过原脚本中佩奇回答的长度"
        ]
    }
}

class PeppaPigEvaluator:
    """Evaluator for Peppa Pig character responses using DeepSeek model"""
    
    def __init__(self):
        self.evaluation_results = []
        
    def evaluate_response(self, response: str, context: str = "", model_name: str = "Unknown") -> Dict:
        """Evaluate a single response based on criteria using DeepSeek"""
        evaluation = {
            "model_name": model_name,
            "response": response,
            "context": context,
            "scores": {},
            "total_score": 0,
            "evaluation_details": {}
        }
        
        # Evaluate against each criterion using DeepSeek
        total_criteria = 0
        total_score = 0
        
        for category, details in EVALUATION_CRITERIA.items():
            category_score = 0
            category_details = []
            
            for criterion in details["sub_criteria"]:
                # Check if the response meets the criterion using DeepSeek
                criterion_score, explanation = self._check_criterion_with_deepseek(response, context, criterion)
                category_score += criterion_score
                category_details.append({
                    "criterion": criterion,
                    "score": criterion_score,
                    "explanation": explanation
                })
                
            # Average score for this category
            avg_score = category_score / len(details["sub_criteria"]) if details["sub_criteria"] else 0
            evaluation["scores"][category] = avg_score
            evaluation["evaluation_details"][category] = category_details
            total_criteria += len(details["sub_criteria"])
            total_score += category_score
            
        # Overall score
        evaluation["total_score"] = total_score / total_criteria if total_criteria > 0 else 0
        
        return evaluation
    
    def _check_criterion_with_deepseek(self, response: str, context: str, criterion: str) -> Tuple[float, str]:
        """Call DeepSeek API to evaluate if response meets a specific criterion"""
        import os
        import json
        
        # Load model configuration from model_configs.json
        model_configs_path = "/model_configs.json"
        
        try:
            with open(model_configs_path, 'r', encoding='utf-8') as f:
                model_configs = json.load(f)
            
            # Find the deepseek-chat model configuration
            deepseek_config = None
            for config in model_configs:
                if config.get("model_name") == "deepseek-chat" or config.get("config_name") == "deepseek-chat":
                    deepseek_config = config
                    break
            
            if not deepseek_config:
                print("警告: 未找到 deepseek-chat 模型配置，使用模拟评估")
                score = 0.5
                explanation = "未找到 deepseek-chat 模型配置"
                return score, explanation
            
            # Extract API key and base URL
            api_key = deepseek_config.get("api_key")
            base_url = deepseek_config.get("client_args", {}).get("base_url")
            model_name = deepseek_config.get("model_name", "deepseek-r1")
            
            if not api_key:
                print("警告: 未找到 deepseek-r1 模型的API密钥，使用模拟评估")
                score = 0.5
                explanation = "未找到API密钥"
                return score, explanation
                
            if not base_url:
                print("警告: 未找到 deepseek-r1 模型的API端点，使用模拟评估")
                score = 0.5
                explanation = "未找到API端点"
                return score, explanation
        
        except FileNotFoundError:
            print(f"警告: 未找到模型配置文件 {model_configs_path}，使用模拟评估")
            score = 0.5
            explanation = "模型配置文件不存在"
            return score, explanation
        except json.JSONDecodeError:
            print(f"警告: 模型配置文件 {model_configs_path} 格式错误，使用模拟评估")
            score = 0.5
            explanation = "模型配置文件格式错误"
            return score, explanation
        except Exception as e:
            print(f"警告: 加载模型配置时出错: {e}，使用模拟评估")
            score = 0.5
            explanation = f"加载模型配置失败: {str(e)}"
            return score, explanation
        
        # Construct the prompt for DeepSeek
        prompt = f"""
        请评估以下小猪佩奇角色的回应是否符合给定的评价标准。

        评价标准: {criterion}
        
        上下文: {context}
        
        需要评估的回应: {response}
        
        请按照以下方式评估：
        1. 根据给定的评价标准，判断回应是否符合要求
        2. 输出一个0到1之间的分数，其中0表示完全不符合，1表示完全符合
        3. 提供简短的解释说明为什么给出这个分数
        
        请严格按照以下JSON格式输出:
        {{
            "score": 0.x,
            "explanation": "你的解释"
        }}
        
        注意：回应必须符合4岁小猪佩奇角色的特征，语气充满兴奋和活力，喜欢用简单直接的句子，
        说话带童趣，表达情绪时很直接，喜欢讲述和家人朋友的有趣故事，经常邀请别人一起玩，
        对新鲜事物充满好奇心，会问很多问题，偶尔会炫耀擅长的事情，有时会以自己的角度理解世界。
        回答必须简洁，每句话不超过12个字，多使用正面积极的词汇，提到跳泥坑时要特别兴奋，
        语气温和友善，充满童趣。不要说任何负面或令人害怕的内容，不要使用复杂难懂的词汇，
        不要提及任何危险活动，不要偏离小猪佩奇的角色设定，不要超出4岁儿童的认知发展水平，
        不要进行长篇解释或说教，不要解释原因，不要说道理，不要长篇大论。
        """
        
        try:
            # Prepare the API call to DeepSeek (using OpenAI-compatible API)
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
            
            # Prepare payload for DeepSeek API (using the deepseek-r1 model)
            payload = {
                "model": model_name,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.1,  # Low temperature for more consistent evaluations
                "max_tokens": 300
            }
            
            # Make the API call
            response = requests.post(f"{base_url}/chat/completions", headers=headers, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                # Parse the JSON response from the model
                try:
                    eval_result = json.loads(content)
                    score = eval_result.get('score', 0.5)
                    explanation = eval_result.get('explanation', '评估完成')
                    return score, explanation
                except json.JSONDecodeError:
                    print(f"警告: 无法解析DeepSeek响应为JSON: {content}")
                    score = 0.5
                    explanation = f"模型响应格式错误: {content[:100]}..."
                    return score, explanation
            else:
                print(f"警告: DeepSeek API调用失败，状态码: {response.status_code}, 响应: {response.text}")
                # Fallback to simple heuristic if API call fails
                score = 0.5
                explanation = f"API调用失败: {response.status_code}"
                return score, explanation
                
        except Exception as e:
            print(f"DeepSeek API调用时出错: {e}")
            # Fallback to simple heuristic if API call fails
            score = 0.5
            explanation = f"API调用异常: {str(e)}"
        
        return score, explanation
    
    def load_evaluation_data(self, filepath: str) -> List[Dict]:
        """Load evaluation data from JSON file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Extract model results
            results = []
            if "model_results" in data:
                for model_result in data["model_results"]:
                    model_name = model_result.get("model_name", "Unknown")
                    for scenario in model_result.get("scenarios", []):
                        for test_case in scenario.get("test_cases", []):
                            results.append({
                                "model_name": model_name,
                                "input": test_case.get("original_input", ""),
                                "expected": test_case.get("expected_response", ""),
                                "generated": test_case.get("generated_response", ""),
                                "similarity": test_case.get("similarity", 0),
                                "positive_guidance": test_case.get("positive_guidance", 0),
                                "passed": test_case.get("passed", False),
                                "scenario": scenario.get("scenario_title", "Unknown")
                            })
            
            return results
        except Exception as e:
            print(f"Error loading evaluation data from {filepath}: {e}")
            return []
    
    def compare_models(self, data_14b: List[Dict], data_32b: List[Dict]) -> Dict:
        """Compare responses from two different models"""
        comparison_results = {
            "timestamp": datetime.now().isoformat(),
            "model_comparison": {},
            "detailed_evaluation": [],
            "summary": {}
        }
        
        # Create model-specific data
        all_data = data_14b + data_32b
        
        for item in all_data:
            model_name = item["model_name"]
            response = item["generated"]
            context = f"Scenario: {item['scenario']}, Input: {item['input']}"
            
            evaluation = self.evaluate_response(response, context, model_name)
            evaluation["original_data"] = item
            comparison_results["detailed_evaluation"].append(evaluation)
        
        # Calculate summary statistics by model
        model_stats = {}
        for eval_item in comparison_results["detailed_evaluation"]:
            model = eval_item["model_name"]
            if model not in model_stats:
                model_stats[model] = {
                    "total_evaluations": 0,
                    "total_score": 0,
                    "avg_similarity": 0,
                    "avg_positive_guidance": 0,
                    "passed_count": 0,
                    "scenarios": set()
                }
            
            stats = model_stats[model]
            stats["total_evaluations"] += 1
            stats["total_score"] += eval_item["total_score"]
            stats["avg_similarity"] += eval_item["original_data"]["similarity"]
            stats["avg_positive_guidance"] += eval_item["original_data"]["positive_guidance"]
            if eval_item["original_data"]["passed"]:
                stats["passed_count"] += 1
            stats["scenarios"].add(eval_item["original_data"]["scenario"])
        
        # Calculate averages
        for model, stats in model_stats.items():
            if stats["total_evaluations"] > 0:
                stats["avg_score"] = stats["total_score"] / stats["total_evaluations"]
                stats["avg_similarity"] = stats["avg_similarity"] / stats["total_evaluations"]
                stats["avg_positive_guidance"] = stats["avg_positive_guidance"] / stats["total_evaluations"]
                stats["pass_rate"] = stats["passed_count"] / stats["total_evaluations"]
            else:
                stats["avg_score"] = 0
                stats["avg_similarity"] = 0
                stats["avg_positive_guidance"] = 0
                stats["pass_rate"] = 0
            
            stats["unique_scenarios"] = len(stats["scenarios"])
            del stats["scenarios"]  # Remove the set before serialization
        
        comparison_results["model_comparison"] = model_stats
        comparison_results["summary"] = self._generate_summary(model_stats)
        
        return comparison_results
    
    def _generate_summary(self, model_stats: Dict) -> Dict:
        """Generate a summary of the comparison"""
        summary = {
            "best_model_by_score": None,
            "best_model_by_similarity": None,
            "best_model_by_guidance": None,
            "best_model_by_pass_rate": None,
            "overall_winner": None
        }
        
        if not model_stats:
            return summary
        
        # Find best model by each metric
        best_by_score = max(model_stats.items(), key=lambda x: x[1]["avg_score"])
        best_by_similarity = max(model_stats.items(), key=lambda x: x[1]["avg_similarity"])
        best_by_guidance = max(model_stats.items(), key=lambda x: x[1]["avg_positive_guidance"])
        best_by_pass_rate = max(model_stats.items(), key=lambda x: x[1]["pass_rate"])
        
        summary["best_model_by_score"] = best_by_score[0]
        summary["best_model_by_similarity"] = best_by_similarity[0]
        summary["best_model_by_guidance"] = best_by_guidance[0]
        summary["best_model_by_pass_rate"] = best_by_pass_rate[0]
        
        # Overall winner based on weighted score
        weighted_scores = {}
        for model, stats in model_stats.items():
            # Calculate weighted score (equal weight for now)
            weighted_score = (
                stats["avg_score"] * 0.3 + 
                stats["avg_similarity"] * 0.25 + 
                stats["avg_positive_guidance"] * 0.25 + 
                stats["pass_rate"] * 0.2
            )
            weighted_scores[model] = weighted_score
        
        summary["overall_winner"] = max(weighted_scores.items(), key=lambda x: x[1])[0]
        
        return summary
    
    def save_results(self, results: Dict, output_path: str):
        """Save evaluation results to JSON file"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"Results saved to {output_path}")
        except Exception as e:
            print(f"Error saving results: {e}")
    
    def print_summary(self, results: Dict):
        """Print a summary of the evaluation results"""
        print("\n" + "="*60)
        print("PEPPA PIG MODEL COMPARISON EVALUATION SUMMARY")
        print("="*60)
        
        summary = results.get("summary", {})
        print(f"Overall Winner: {summary.get('overall_winner', 'N/A')}")
        print(f"Best by Score: {summary.get('best_model_by_score', 'N/A')}")
        print(f"Best by Similarity: {summary.get('best_model_by_similarity', 'N/A')}")
        print(f"Best by Guidance: {summary.get('best_model_by_guidance', 'N/A')}")
        print(f"Best by Pass Rate: {summary.get('best_model_by_pass_rate', 'N/A')}")
        
        print("\nModel Comparison Details:")
        print("-" * 60)
        
        model_comparison = results.get("model_comparison", {})
        for model, stats in model_comparison.items():
            print(f"\nModel: {model}")
            print(f"  Average Evaluation Score: {stats.get('avg_score', 0):.3f}")
            print(f"  Average Similarity: {stats.get('avg_similarity', 0):.3f}")
            print(f"  Average Positive Guidance: {stats.get('avg_positive_guidance', 0):.3f}")
            print(f"  Pass Rate: {stats.get('pass_rate', 0):.3f}")
            print(f"  Total Evaluations: {stats.get('total_evaluations', 0)}")
            print(f"  Scenarios Covered: {stats.get('unique_scenarios', 0)}")


def extract_qs_data(filepath: str, model_identifier: str = None) -> List[Dict]:
    """Extract model responses from qs.txt file format with model identification"""
    data = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract model responses
        # Pattern: [timestamp] Model: model_name\nQ: question\nA: answer\n--------------------------------------------------
        pattern = r'\[.*?\] Model: (.*?)\nQ: (.*?)\nA: (.*?)\n-{50,}'
        matches = re.findall(pattern, content, re.DOTALL)
        
        for match in matches:
            model_name = match[0].strip()
            question = match[1].strip()
            answer = match[2].strip()
            
            # If a specific model identifier was provided, only include matches from that model
            if model_identifier and model_identifier not in model_name:
                continue
                
            data.append({
                "model_name": model_name,
                "input": question,
                "generated": answer,
                "expected": "",  # Not available in this format
                "similarity": 0,  # Not available in this format
                "positive_guidance": 0,  # Not available in this format
                "passed": False,  # Not available in this format
                "scenario": f"Extracted from {os.path.basename(filepath)}"  # Show which file it came from
            })
                
    except Exception as e:
        print(f"Error extracting data from {filepath}: {e}")
    
    return data


def main():
    parser = argparse.ArgumentParser(description="Peppa Pig Model Comparison Evaluator")
    parser.add_argument("--qs-file", type=str,
                       default="/Users/miulujing/Documents/pycharmProject/luna/result/logs/qs.txt",
                       help="Path to qs.txt file with model responses")
    parser.add_argument("--qs-old-file", type=str,
                       default="/Users/miulujing/Documents/pycharmProject/luna/result/qs1007.txt",
                       help="Path to qs1007.txt file with model responses")
    parser.add_argument("--output", type=str,
                       default="/Users/miulujing/Documents/pycharmProject/luna/result/peppa_model_comparison.json",
                       help="Output path for comparison results")
    
    args = parser.parse_args()
    
    evaluator = PeppaPigEvaluator()
    
    print("Loading evaluation data...")
    
    # Extract data from both qs files
    print(f"Loading data from: {args.qs_file}")
    data_qs = extract_qs_data(args.qs_file)
    print(f"Extracted {len(data_qs)} items from qs.txt")
    
    print(f"Loading data from: {args.qs_old_file}")
    data_qs_old = extract_qs_data(args.qs_old_file)
    print(f"Extracted {len(data_qs_old)} items from qs1007.txt")
    
    # Separate data by file and model type for proper comparison
    # qs.txt data
    qs_14b = []
    qs_32b = []
    
    for item in data_qs:
        if "14B" in item["model_name"]:
            qs_14b.append(item)
        elif "32B" in item["model_name"]:
            qs_32b.append(item)
    
    # qs1007.txt data
    qs_old_14b = []
    qs_old_32b = []
    
    for item in data_qs_old:
        if "14B" in item["model_name"]:
            qs_old_14b.append(item)
        elif "32B" in item["model_name"]:
            qs_old_32b.append(item)
    
    print(f"Identified {len(qs_14b)} items for 14B model from qs.txt")
    print(f"Identified {len(qs_32b)} items for 32B model from qs.txt")
    print(f"Identified {len(qs_old_14b)} items for 14B model from qs1007.txt")
    print(f"Identified {len(qs_old_32b)} items for 32B model from qs1007.txt")
    
    # According to the requirement: compare 14B from qs.txt vs 14B from qs1007.txt
    print("Performing comparison: 14B from qs.txt vs 14B from qs1007.txt...")
    results = evaluator.compare_models(qs_14b, qs_old_14b)
    
    # Alternative: if you want to compare all 14B models vs all 32B models regardless of source file:
    # data_14b = qs_14b + qs_old_14b
    # data_32b = qs_32b + qs_old_32b
    # results = evaluator.compare_models(data_14b, data_32b)
    
    # Save results
    evaluator.save_results(results, args.output)
    
    # Print summary
    evaluator.print_summary(results)
    
    print(f"\nDetailed results saved to: {args.output}")


if __name__ == "__main__":
    main()