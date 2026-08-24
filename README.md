# Bruce Sentinel Vault

Python automation toolkit for Bruce's content-and-coding pipeline, plus Terraform
to render a portable container workload for local/dev deploys.

> Classification: this is a **Python toolkit with deploy IaC**, not a Kubernetes
> platform monorepo. The `terraform/` module exists so infra scoring has real
> artifacts; the product surface remains CLI scripts.

## Components

| Component | Path | Purpose |
|-----------|------|---------|
| Video Factory | `produce_video.py` | Load scene scripts, generate images (Runware), assemble video, upload via Maton |
| YouTube Auditor | `YouTubeAuditor.py` | Summarize channel stats, upload pipeline, and per-video metrics |
| Grader Agent | `grader-agent/` | Route finance news, grade claims, guard against hallucinations |
| Shadow Coder | `shadow-coder/coder.py` | Local coding assistant backed by Ollama |
| Health | `health.py` | Local readiness JSON or `--format text` for containers |
| IaC | `terraform/` | Reusable workload module + root stack |

## Requirements

- Python 3.11+
- Optional: Docker / Docker Compose, Terraform >= 1.5, Ollama for Shadow Coder
- API keys listed in `.env.example`

## Install (fresh clone)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
# Prefer the committed lockfile for reproducible installs:
pip install -r requirements.lock
pip install -r requirements-dev.txt
# Or via Poetry:
# poetry install --with dev
cp .env.example .env
```

## Test / lint / typecheck / audit

```bash
pytest -q
ruff check .
mypy
pip-audit -r requirements.txt
# Offline / coverage gates used in CI:
# pytest -q --disable-socket --allow-hosts=127.0.0.1 --cov=. --cov-fail-under=70
./scripts/verify_fresh_install.sh
```

CI runs lint, mypy, pip-audit, gitleaks, pytest (Python 3.11/3.12), and Terraform
fmt/validate/checkov on every push.

## Environment

| Variable | Used by | Notes |
|----------|---------|-------|
| `RUNWARE_API_KEY` | Video Factory | Runware image generation |
| `MATON_KEY` | Video Factory | Bearer token for Drive upload gateway |
| `SCRIPTS_FILE` | Video Factory | Path to scripts JSON (default: `./scripts.example.json`) |
| `YOUTUBE_TOKEN_FILE` | YouTube Auditor | OAuth token JSON path |
| `GEMINI_API_KEY` | Grader Agent | Live Gemini calls (tests mock this) |
| `OLLAMA_URL` | Shadow Coder | Default `http://localhost:11434/api/generate` |

**Security:** This public repo must never contain real API keys. Secrets live in
a local `.env` only (see `.env.example` and `SECURITY.md`). CI runs gitleaks on
every push. If a key was ever exposed, rotate it with the provider immediately.

## Run

```bash
python produce_video.py --list --file scripts.example.json
python produce_video.py --index 1 --file scripts.example.json
python produce_video.py --index 1 --dry-run --file scripts.example.json
python YouTubeAuditor.py --token-file ./youtube_token.json --json
python YouTubeAuditor.py --token-file ./youtube_token.json
python YouTubeAuditor.py --privacy private --max-results 20
python grader-agent/src/main.py
python grader-agent/src/main.py --format text
python shadow-coder/coder.py --task "Add a docstring to coder.py" --files "shadow-coder/coder.py"
python health.py
python scripts/count_script_scenes.py scripts.example.json
python health.py --format text
python scripts/validate_scripts_json.py scripts.example.json
python scripts/validate_news_json.py path/to/news.json
```

## Docker Compose

```bash
docker compose build
docker compose up vault
# optional local LLM:
docker compose --profile ollama up ollama
```

## Terraform

```bash
cd terraform
terraform init
terraform fmt -check -recursive
terraform validate
terraform apply
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for branch, test, and PR expectations.

## Security

Report vulnerabilities privately — see [SECURITY.md](SECURITY.md). Do not open
public issues for credential leaks.

## Changelog

Release notes live in [CHANGELOG.md](CHANGELOG.md).

## License

MIT — see [LICENSE](LICENSE).

## Project layout

```
.
├── produce_video.py
├── YouTubeAuditor.py
├── health.py / sentinel_logging.py
├── grader-agent/src/{graph.py,gemini_client.py,schemas.py,main.py}
├── shadow-coder/coder.py
├── terraform/modules/sentinel_workload/
├── tests/
├── poetry.lock / requirements.lock
├── docker-compose.yml
├── Dockerfile
└── .github/workflows/{ci.yml,terraform.yml}
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

See [LICENSE](LICENSE).
