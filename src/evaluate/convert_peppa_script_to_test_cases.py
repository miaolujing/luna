#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Convert Peppa Pig script to structured JSON test cases
Transforms script into "context-Peppa response" test pairs
Each scene is contained within a large collection
"""

import json
import re
import os
from typing import List, Dict, Any

def parse_script_content(content: str) -> List[Dict[str, Any]]:
    """
    Parse the script content and extract scenes with dialogues
    
    Args:
        content: The raw script content
        
    Returns:
        List of scenes with their dialogues
    """
    # Normalize line endings
    content = content.replace('\r\n', '\n').replace('\r', '\n')
    
    # Split content by episode headers (## followed by episode number and title)
    scenes = re.split(r'\n##\s+', content)
    
    # Remove the first element which might just be text before the first episode
    if scenes and not scenes[0].strip().startswith(("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")):
        scenes.pop(0)
    
    # Add back the header to each scene
    formatted_scenes = []
    for scene in scenes:
        if scene.strip():
            # Add back the ## header
            formatted_scene = "## " + scene
            formatted_scenes.append(formatted_scene)
    
    parsed_scenes = []
    
    for scene in formatted_scenes:
        # Extract scene lines
        scene_lines = scene.split('\n')
        scene_title = scene_lines[0].replace('##', '').strip() if scene_lines else "Unknown Scene"
        
        # Parse dialogues
        dialogues = []
        for line in scene_lines[1:]:  # Skip the title line
            line = line.strip()
            if not line:
                continue
                
            # Check if this line is a dialogue line (**Speaker:** format)
            dialogue_match = re.match(r'\*\*(.+?)[：:]\*\*\s*(.+)', line)
            if dialogue_match:
                speaker = dialogue_match.group(1)
                content = dialogue_match.group(2)
                dialogues.append({
                    'speaker': speaker,
                    'content': content
                })
            elif line.startswith('**旁白**') or line.startswith('**旁白：**') or line.startswith('**旁白:**'):
                # Handle narrator content
                narrator_content = line.replace('**旁白**', '').replace('**旁白：**', '').replace('**旁白:**', '').strip()
                if narrator_content:
                    dialogues.append({
                        'speaker': '旁白',
                        'content': narrator_content
                    })
        
        parsed_scenes.append({
            'title': scene_title,
            'dialogues': dialogues
        })
    
    return parsed_scenes

def extract_peppa_responses(scenes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Extract all of Peppa's lines from scenes and create test cases
    
    Args:
        scenes: List of parsed scenes
        
    Returns:
        List of test cases with context and expected responses
    """
    test_cases = []
    
    for scene in scenes:
        scene_title = scene['title']
        dialogues = scene['dialogues']
        
        # Find all Peppa's responses - match only exact "佩奇" or "小猪佩奇", not phrases like "佩奇的朋友们"
        peppa_indices = []
        for i, dialogue in enumerate(dialogues):
            speaker = dialogue['speaker'].strip()
            # Only match exact speaker names that are "佩奇" or "小猪佩奇"
            if speaker in ['佩奇', '小猪佩奇']:
                peppa_indices.append(i)
        
        # For each Peppa response, determine the triggering context
        scene_test_cases = []
        for idx in peppa_indices:
            peppa_response = dialogues[idx]['content']
            
            # Determine context by backtracking from this specific Peppa response
            context_lines = []
            
            # Look for the most recent non-Peppa dialogues before this response
            # First, find the previous Peppa response (if any) to limit our search
            prev_peppa_idx = -1
            for prev_idx in reversed(peppa_indices):
                if prev_idx < idx:
                    prev_peppa_idx = prev_idx
                    break
            
            # Start looking from the dialogue before this Peppa response
            # Stop when we reach the previous Peppa response or the beginning
            i = idx - 1
            while i > prev_peppa_idx and len(context_lines) < 5:  # Limit to 5 lines to prevent too much context
                prev_dialogue = dialogues[i]
                
                # Skip only this exact Peppa response, but include other characters (including "佩奇的朋友们")
                # Only exclude if the speaker is exactly "佩奇" or "小猪佩奇"
                prev_speaker = prev_dialogue['speaker'].strip()
                if prev_speaker not in ['佩奇', '小猪佩奇']:
                    # Add non-Peppa dialogues to context
                    if prev_dialogue['speaker'] == '旁白':
                        context_lines.insert(0, f"旁白：{prev_dialogue['content']}")
                    else:
                        context_lines.insert(0, f"{prev_dialogue['speaker']}说：{prev_dialogue['content']}")
                
                i -= 1
            
            # Create context string
            context = "\n".join(context_lines) if context_lines else "（无上下文）"
            
            # Create test case
            test_case = {
                "context": context,
                "expected_response": peppa_response,
                "scene": scene_title,
                "dialogue_index": idx
            }
            
            scene_test_cases.append(test_case)
        
        test_cases.extend(scene_test_cases)
    
    return test_cases

def group_test_cases_by_scene(test_cases: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Group test cases by scene
    
    Args:
        test_cases: List of all test cases
        
    Returns:
        Dictionary with scenes as keys and test cases as values
    """
    grouped_cases = {}
    
    for test_case in test_cases:
        scene = test_case['scene']
        if scene not in grouped_cases:
            grouped_cases[scene] = []
        grouped_cases[scene].append(test_case)
    
    return grouped_cases

def convert_script_to_json_test_cases(input_file: str, output_file: str):
    """
    Convert Peppa Pig script to structured JSON test cases
    
    Args:
        input_file: Path to the input script file
        output_file: Path to the output JSON file
    """
    # Read the script file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse scenes
    scenes = parse_script_content(content)
    
    # Extract Peppa's responses and create test cases
    test_cases = extract_peppa_responses(scenes)
    
    # Group test cases by scene
    grouped_test_cases = group_test_cases_by_scene(test_cases)
    
    # Create final structure
    result = {
        "info": {
            "source": input_file,
            "total_scenes": len(grouped_test_cases),
            "total_test_cases": len(test_cases),
            "conversion_timestamp": __import__('datetime').datetime.now().isoformat()
        },
        "test_cases_by_scene": grouped_test_cases,
        "all_test_cases": test_cases
    }
    
    # Write to JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully converted {len(test_cases)} test cases from {len(grouped_test_cases)} scenes")
    print(f"Output saved to: {output_file}")
    
    # Print summary
    print("\nSummary:")
    print(f"  Total scenes: {len(grouped_test_cases)}")
    print(f"  Total test cases: {len(test_cases)}")
    print("\nTest cases by scene:")
    for scene, cases in grouped_test_cases.items():
        print(f"  {scene}: {len(cases)} test cases")

def main():
    """Main function to run the conversion"""
    # Define file paths
    input_file = "../../result/testCase/测试脚本.md"
    output_file = "../../result/testCase/peppa_structured_test_cases.json"
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file not found: {input_file}")
        return
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Convert script to JSON test cases
    try:
        convert_script_to_json_test_cases(input_file, output_file)
        print("\nConversion completed successfully!")
    except Exception as e:
        print(f"Error during conversion: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()