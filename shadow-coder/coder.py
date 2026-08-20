"""Shadow-Coder: local Ollama-powered coding assistant."""

from __future__ import annotations

import argparse
import logging
import os
import sys
from collections.abc import Callable
from pathlib import Path

import requests

# Repo root on sys.path for shared logging helper.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

logger = logging.getLogger(__name__)

DEFAULT_OLLAMA_URL = "http://localhost:11434/api/generate"


class OllamaError(RuntimeError):
    """Raised when the local Ollama endpoint cannot be reached or responds badly."""


def get_file_content(filepath: str) -> str:
    try:
        with open(filepath, encoding="utf-8") as handle:
            return handle.read()
    except OSError as exc:
        logger.exception("Failed to read %s", filepath)
        raise OllamaError(f"Error reading {filepath}: {exc}") from exc


def parse_ollama_response(payload: dict) -> str:
    """Extract the model text from an Ollama /api/generate JSON body."""
    if not isinstance(payload, dict):
        raise ValueError("Ollama response must be a JSON object")
    text = payload.get("response")
    if text is None:
        return "No response from model."
    return str(text)


def run_shadow_coder(
    task: str,
    files: list[str],
    model: str = "qwen2.5:7b",
    ollama_url: str | None = None,
    post: Callable[..., requests.Response] | None = None,
) -> str:
    """Ask a local Ollama model to implement `task` given optional file context."""
    context = ""
    for path in files:
        content = get_file_content(path)
        context += f"\n--- FILE: {path} ---\n{content}\n"

    system_prompt = """You are Shadow-Coder, a senior software engineer assistant. 
Your task is to provide code modifications or new code based on the user's request.
Always output the full content of the modified files within triple backticks, preceded by the filename.
Format:
FILE: path/to/file
```
code here
```
Be precise, efficient, and follow best practices."""

    prompt = (
        f"TASK: {task}\n\nCONTEXT FILES:\n{context}\n\n"
        "Provide the implementation/modifications."
    )

    payload = {
        "model": model,
        "prompt": prompt,
        "system": system_prompt,
        "stream": False,
    }

    url = ollama_url or os.environ.get("OLLAMA_URL") or DEFAULT_OLLAMA_URL
    http_post = post or requests.post

    logger.info("Shadow-Coder is thinking (using %s)...", model)
    try:
        response = http_post(url, json=payload, timeout=300)
        response.raise_for_status()
        return parse_ollama_response(response.json())
    except OllamaError:
        raise
    except Exception as exc:
        logger.exception("Error connecting to Ollama at %s", url)
        raise OllamaError(f"Error connecting to Ollama: {exc}") from exc


def main(argv=None) -> int:
    from sentinel_logging import configure_logging

    configure_logging()
    parser = argparse.ArgumentParser(description="Shadow-Coder: Local Coding Assistant")
    parser.add_argument("--task", required=True, help="The coding task to perform")
    parser.add_argument(
        "--files",
        help="Comma-separated list of file paths to include as context",
    )
    parser.add_argument("--model", default="qwen2.5:7b", help="Ollama model to use")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Automatically try to apply changes (experimental)",
    )
    args = parser.parse_args(argv)

    file_list: list[str] = []
    if args.files:
        file_list = [f.strip() for f in args.files.split(",") if f.strip()]

    try:
        response = run_shadow_coder(args.task, file_list, args.model)
    except OllamaError as exc:
        logger.error("%s", exc)
        return 1
    print("\n--- SHADOW-CODER OUTPUT ---")
    print(response)
    print("\n--- END OF OUTPUT ---")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
