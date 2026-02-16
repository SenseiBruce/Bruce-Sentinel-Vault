import os
import sys
import json
import argparse
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def get_file_content(filepath):
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error reading {filepath}: {str(e)}"

def run_shadow_coder(task, files, model="qwen2.5:7b"):
    context = ""
    for f in files:
        content = get_file_content(f)
        context += f"\n--- FILE: {f} ---\n{content}\n"

    system_prompt = """You are Shadow-Coder, a senior software engineer assistant. 
Your task is to provide code modifications or new code based on the user's request.
Always output the full content of the modified files within triple backticks, preceded by the filename.
Format:
FILE: path/to/file
```
code here
```
Be precise, efficient, and follow best practices."""

    prompt = f"TASK: {task}\n\nCONTEXT FILES:\n{context}\n\nProvide the implementation/modifications."

    payload = {
        "model": model,
        "prompt": prompt,
        "system": system_prompt,
        "stream": False
    }

    print(f"Shadow-Coder is thinking (using {model})...")
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=300)
        response.raise_for_status()
        result = response.json()
        return result.get("response", "No response from model.")
    except Exception as e:
        return f"Error connecting to Ollama: {str(e)}"

def main():
    parser = argparse.ArgumentParser(description="Shadow-Coder: Local Coding Assistant")
    parser.add_argument("--task", required=True, help="The coding task to perform")
    parser.add_argument("--files", help="Comma-separated list of file paths to include as context")
    parser.add_argument("--model", default="qwen2.5:7b", help="Ollama model to use")
    parser.add_argument("--apply", action="store_true", help="Automatically try to apply changes (experimental)")

    args = parser.parse_args()
    
    file_list = []
    if args.files:
        file_list = [f.strip() for f in args.files.split(",")]

    response = run_shadow_coder(args.task, file_list, args.model)
    
    print("\n--- SHADOW-CODER OUTPUT ---")
    print(response)
    print("\n--- END OF OUTPUT ---")

if __name__ == "__main__":
    main()
