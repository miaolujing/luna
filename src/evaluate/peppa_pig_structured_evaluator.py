#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Peppa Pig Structured Evaluator
Loads test cases from structured JSON file and evaluates model responses using multiple metrics
"""

import json
import re
import time
import requests
import sys
import os
import csv
from urllib.parse import urljoin
from difflib import SequenceMatcher
from datetime import datetime

# Try to import Chinese text processing libraries
try:
    import jieba
    JIEBA_AVAILABLE = True
except ImportError:
    JIEBA_AVAILABLE = False
    print("Warning: jieba not available. Chinese word-level similarity will not be calculated.")

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    print("Warning: scikit-learn not available. TF-IDF similarity will not be calculated.")

# Try to import Sentence-BERT for semantic similarity
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_BERT_AVAILABLE = True
except ImportError:
    SENTENCE_BERT_AVAILABLE = False
    print("Warning: sentence-transformers not available. Sentence-BERT similarity will not be calculated.")

def load_structured_test_cases(file_path):
    """
    Load structured test cases from JSON file
    
    Args:
        file_path: Path to the structured test cases JSON file
        
    Returns:
        Dictionary of test cases grouped by scene
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Return test cases grouped by scene
        return data.get('test_cases_by_scene', {})
    except FileNotFoundError:
        print(f"Error: Test case file not found: {file_path}")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in test case file: {e}")
        return {}
    except Exception as e:
        print(f"Error loading test cases: {e}")
        return {}

def call_chat_api(context, model_name, server_url="http://localhost:8000"):
    """
    Call the Peppa Pig chat API with context
    
    Args:
        context: The context to send to the model
        model_name: Name of the model to use
        server_url: URL of the chat server
        
    Returns:
        Generated response or None if error
    """
    try:
        response = requests.post(
            url=urljoin(server_url, '/chat'),
            json={
                'message': context,
                'model_config_name': model_name
            },
            headers={'Content-Type': 'application/json'},
            timeout=60  # 60 second timeout
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get('response', '')
        else:
            print(f"Error: Server returned status {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"Error making request to server: {e}")
        return None

def reset_conversation(server_url="http://localhost:8000"):
    """
    Reset the conversation history on the server
    
    Args:
        server_url: URL of the chat server
        
    Returns:
        Boolean indicating success
    """
    try:
        response = requests.post(
            url=urljoin(server_url, '/reset'),
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            print("Conversation history reset successfully.")
            return True
        else:
            print(f"Error resetting conversation: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"Error resetting conversation: {e}")
        return False

def calculate_exact_match(expected, predicted):
    """
    Calculate exact match accuracy
    
    Args:
        expected: Expected response
        predicted: Predicted response
        
    Returns:
        Float representing exact match score (0.0 or 1.0)
    """
    return 1.0 if expected.strip() == predicted.strip() else 0.0

def calculate_fuzzy_match(expected, predicted):
    """
    Calculate fuzzy match similarity using SequenceMatcher
    
    Args:
        expected: Expected response
        predicted: Predicted response
        
    Returns:
        Float representing fuzzy match score (0.0 to 1.0)
    """
    return SequenceMatcher(None, expected, predicted).ratio()

def calculate_edit_distance(expected, predicted):
    """
    Calculate normalized edit distance
    
    Args:
        expected: Expected response
        predicted: Predicted response
        
    Returns:
        Float representing normalized edit distance (0.0 to 1.0, where 1.0 is identical)
    """
    from difflib import SequenceMatcher
    # Using SequenceMatcher's ratio as it's essentially normalized edit distance
    return SequenceMatcher(None, expected, predicted).ratio()

def calculate_sentence_bert_similarity(expected, predicted):
    """
    Calculate Sentence-BERT similarity
    
    Args:
        expected: Expected response
        predicted: Predicted response
        
    Returns:
        Float representing semantic similarity (0.0 to 1.0)
    """
    if not SENTENCE_BERT_AVAILABLE:
        return 0.0
    
    try:
        model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        embeddings = model.encode([expected, predicted])
        similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
        return float(similarity)
    except Exception as e:
        print(f"Error calculating Sentence-BERT similarity: {e}")
        return 0.0

def calculate_keyword_similarity(expected, predicted):
    """
    Calculate keyword-based similarity
    
    Args:
        expected: Expected response
        predicted: Predicted response
        
    Returns:
        Float representing keyword similarity (0.0 to 1.0)
    """
    try:
        # Extract keywords (simple approach: split by common separators)
        if JIEBA_AVAILABLE:
            expected_keywords = set(jieba.cut(expected))
            predicted_keywords = set(jieba.cut(predicted))
        else:
            # Simple whitespace-based splitting for English or fallback
            expected_keywords = set(expected.split())
            predicted_keywords = set(predicted.split())
        
        # Remove empty strings
        expected_keywords.discard('')
        predicted_keywords.discard('')
        
        if not expected_keywords and not predicted_keywords:
            return 1.0
        if not expected_keywords or not predicted_keywords:
            return 0.0
            
        # Calculate Jaccard similarity
        intersection = expected_keywords.intersection(predicted_keywords)
        union = expected_keywords.union(predicted_keywords)
        return len(intersection) / len(union)
    except Exception as e:
        print(f"Error calculating keyword similarity: {e}")
        return 0.0

def evaluate_response_metrics(expected, predicted):
    """
    Evaluate response using multiple metrics
    
    Args:
        expected: Expected response
        predicted: Predicted response
        
    Returns:
        Dictionary containing all evaluation metrics
    """
    metrics = {
        'exact_match': calculate_exact_match(expected, predicted),
        'fuzzy_match': calculate_fuzzy_match(expected, predicted),
        'edit_distance': calculate_edit_distance(expected, predicted),
        'sentence_bert': calculate_sentence_bert_similarity(expected, predicted),
        'keyword_similarity': calculate_keyword_similarity(expected, predicted)
    }
    
    # Calculate综合 score (weighted average)
    weights = {
        'exact_match': 0.5,
        'fuzzy_match': 0.2,
        'edit_distance': 0.1,
        'sentence_bert': 0.1,
        'keyword_similarity': 0.1
    }
    
    combined_score = sum(metrics[key] * weights[key] for key in weights)
    metrics['combined_score'] = combined_score
    
    return metrics

def generate_human_annotation_csv(evaluation_results, output_path):
    """
    Generate CSV file for human annotation
    
    Args:
        evaluation_results: List of evaluation results
        output_path: Path to output CSV file
    """
    fieldnames = [
        '场景', '对话索引', '上下文', '期望响应', 
        '实际响应', '模型名称', '完全匹配', '语义相似度', '内容正确性', '风格一致性', '备注'
    ]
    
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for result in evaluation_results:
                # For human annotation fields, we'll leave them blank for manual filling
                row = {
                    '场景': result.get('scene', ''),
                    '对话索引': result.get('dialogue_index', ''),
                    '上下文': result.get('context', ''),
                    '期望响应': result.get('expected_response', ''),
                    '实际响应': result.get('prediction', ''),
                    '模型名称': result.get('model', ''),
                    '完全匹配': result.get('metrics', {}).get('exact_match', 0),
                    '语义相似度': result.get('metrics', {}).get('sentence_bert', 0),
                    '内容正确性': '',  # To be filled by human annotator
                    '风格一致性': '',  # To be filled by human annotator
                    '备注': ''  # To be filled by human annotator
                }
                writer.writerow(row)
        
        print(f"Human annotation CSV saved to: {output_path}")
    except Exception as e:
        print(f"Error generating human annotation CSV: {e}")

def run_structured_evaluation():
    """
    Run structured evaluation using test cases from JSON file
    """
    print("Starting Peppa Pig Structured Evaluation...")
    
    # Load structured test cases
    test_cases_file = "../../result/testCase/peppa_structured_test_cases.json"
    test_cases_by_scene = load_structured_test_cases(test_cases_file)
    
    if not test_cases_by_scene:
        print("No test cases found. Exiting.")
        return
    
    print(f"Loaded {len(test_cases_by_scene)} scenes with {sum(len(cases) for cases in test_cases_by_scene.values())} test cases.")
    
    # Models to evaluate
    models_to_test = ['qwen3-32B']
    
    # Store all evaluation results
    all_evaluation_results = []
    
    # Evaluate each model
    for model_name in models_to_test:
        print(f"\nEvaluating model: {model_name}")
        model_results = []
        
        # Process each scene
        for scene_name, test_cases in test_cases_by_scene.items():
            print(f"  Processing scene: {scene_name} ({len(test_cases)} test cases)")
            
            # Process each test case in the scene
            for i, test_case in enumerate(test_cases):
                context = test_case.get('context', '')
                expected_response = test_case.get('expected_response', '')
                dialogue_index = test_case.get('dialogue_index', i)
                
                print(f"    Test case {i+1}/{len(test_cases)}: Sending context to model...")
                
                # Call the chat API
                predicted_response = call_chat_api(context, model_name)
                
                if predicted_response is None:
                    print("    Failed to get response from server.")
                    continue
                
                # Evaluate response using multiple metrics
                metrics = evaluate_response_metrics(expected_response, predicted_response)
                
                # Store result
                result = {
                    'model': model_name,
                    'scene': scene_name,
                    'dialogue_index': dialogue_index,
                    'context': context,
                    'expected_response': expected_response,
                    'prediction': predicted_response,
                    'metrics': metrics
                }
                
                model_results.append(result)
                all_evaluation_results.append(result)
                
                print(f"    Metrics - Exact: {metrics['exact_match']:.4f}, Fuzzy: {metrics['fuzzy_match']:.4f}, BERT: {metrics['sentence_bert']:.4f}")
            
            # Reset conversation after each scene
            print(f"  Resetting conversation after scene: {scene_name}")
            reset_conversation()
        
        print(f"  Completed evaluation for {model_name}: {len(model_results)} test cases")
    
    # Generate reports with timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M")
    
    # Generate human annotation CSV
    csv_path = f"../../result/peppa_structured_evaluation_{timestamp}_human_annotation.csv"
    generate_human_annotation_csv(all_evaluation_results, csv_path)
    
    # Generate detailed JSON report
    report_data = {
        'evaluation_info': {
            'timestamp': datetime.now().isoformat(),
            'models_evaluated': models_to_test,
            'total_test_cases': len(all_evaluation_results)
        },
        'results': all_evaluation_results
    }
    
    report_path = f"../../result/peppa_structured_evaluation_{timestamp}_report.json"
    try:
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2, default=str)
        print(f"Detailed report saved to: {report_path}")
    except Exception as e:
        print(f"Error saving detailed report: {e}")
    
    # Generate summary report
    summary_path = f"../../result/peppa_structured_evaluation_{timestamp}_summary.txt"
    try:
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write("PEPPA PIG STRUCTURED EVALUATION SUMMARY\n")
            f.write("=" * 50 + "\n")
            f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write(f"Models evaluated: {', '.join(models_to_test)}\n")
            f.write(f"Total test cases: {len(all_evaluation_results)}\n\n")
            
            # Summary by model
            for model_name in models_to_test:
                model_results = [r for r in all_evaluation_results if r['model'] == model_name]
                if model_results:
                    avg_exact = sum(r['metrics']['exact_match'] for r in model_results) / len(model_results)
                    avg_fuzzy = sum(r['metrics']['fuzzy_match'] for r in model_results) / len(model_results)
                    avg_bert = sum(r['metrics']['sentence_bert'] for r in model_results) / len(model_results)
                    
                    f.write(f"\n{model_name}:\n")
                    f.write(f"  Test cases: {len(model_results)}\n")
                    f.write(f"  Average exact match: {avg_exact:.4f}\n")
                    f.write(f"  Average fuzzy match: {avg_fuzzy:.4f}\n")
                    f.write(f"  Average BERT similarity: {avg_bert:.4f}\n")
        
        print(f"Summary report saved to: {summary_path}")
    except Exception as e:
        print(f"Error saving summary report: {e}")
    
    print("\nEvaluation completed successfully!")

if __name__ == "__main__":
    # Run the structured evaluation when script is executed directly
    run_structured_evaluation()