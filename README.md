# Bruce Sentinel Vault

Toolkit for Bruce's content-and-coding pipeline: a video production factory, a YouTube channel auditor, a finance news grader agent, and a local Ollama coding assistant.

## Components

| Component | Path | Purpose |
|-----------|------|---------|
| Video Factory | `produce_video.py` | Load scene scripts, generate images (Runware), assemble video, upload via Maton |
| YouTube Auditor | `YouTubeAuditor.py` | Summarize channel stats, upload pipeline, and per-video metrics |
| Grader Agent | `grader-agent/` | Route finance news, grade claims, guard against hallucinations |
| Shadow Coder | `shadow-coder/coder.py` | Local coding assistant backed by Ollama |

These tools are related by workflow (research → grade → produce → audit) but can be run independently.

## Requirements

- Python 3.11+
- Optional: Ollama running locally for Shadow Coder
- API keys listed in `.env.example`

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

Copy environment defaults:

```bash
cp .env.example .env
# edit .env — never commit real keys
```

## Environment

| Variable | Used by | Notes |
|----------|---------|-------|
| `RUNWARE_API_KEY` | Video Factory | Runware image generation |
| `MATON_KEY` | Video Factory | Bearer token for Drive upload gateway |
| `SCRIPTS_FILE` | Video Factory | Path to scripts JSON (default: `./scripts.example.json`) |
| `YOUTUBE_TOKEN_FILE` | YouTube Auditor | OAuth token JSON path |
| `GEMINI_API_KEY` | Grader Agent | Live Gemini calls (tests mock this) |
| `OLLAMA_URL` | Shadow Coder | Default `http://localhost:11434/api/generate` |

See `.env.example` for placeholders.

**Security note:** Older commits may contain plaintext keys. Rotate `RUNWARE_API_KEY` and `MATON_KEY` with the providers if those values were ever shared.

## Run

```bash
# Video factory (uses SCRIPTS_FILE or --file)
python produce_video.py --index 1 --file scripts.example.json

# YouTube auditor
python YouTubeAuditor.py --token-file ./youtube_token.json

# Grader agent (optional news_input.json in CWD)
python grader-agent/src/main.py

# Shadow coder (requires local Ollama)
python shadow-coder/coder.py --task "Add a docstring to coder.py" --files "shadow-coder/coder.py"
```

## Test

```bash
pytest -q
```

CI runs the same command on every push and pull request.

## Lint

```bash
ruff check .
```

## Docker

```bash
docker build -t bruce-sentinel-vault .
docker run --rm bruce-sentinel-vault pytest -q
```

## Project layout

```
.
├── produce_video.py
├── YouTubeAuditor.py
├── grader-agent/src/{graph.py,gemini_client.py,main.py}
├── shadow-coder/coder.py
├── tests/
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
├── Dockerfile
└── .github/workflows/ci.yml
```
