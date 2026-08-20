# Changelog

## 0.1.2

- Purge leaked Runware/Maton key material from git history; scrub TOOLS.md.
- Add retry helper and in-memory metrics registry with unit tests.
- Health CLI `--fail-on-degraded`; reject unknown grader tasks with ValueError.

## 0.1.1

- Add `poetry.lock` and regenerate `requirements.lock` for reproducible installs.
- Add Terraform `sentinel_workload` module + fmt/validate/checkov CI.
- Broaden CI: Python 3.11/3.12 matrix, mypy, pip-audit, gitleaks.
- Add pydantic schemas for news/scripts entry points with tests.
- Add docker-compose, devcontainer, health endpoint, structured JSON logging.
- Deduplicate YouTube auditor playlist fetching; raise typed Ollama errors.
- Add Dependabot + pre-commit hooks.

## 0.1.0

- Initial hardened toolkit: pytest suite, env-based secrets, README, Dockerfile, CI.
