# Changelog

## Unreleased

- Remove hardcoded API keys and machine-specific paths; load config from environment.
- Add dependency manifests (`requirements.txt`, `requirements-dev.txt`, `pyproject.toml`).
- Add pytest suite for grader-agent, shadow-coder, video factory config, and YouTube auditor.
- Add GitHub Actions CI (pytest + ruff), Dockerfile, README, and `.env.example`.
- Introduce injectable Gemini/DDGS/Ollama clients and structured logging.
