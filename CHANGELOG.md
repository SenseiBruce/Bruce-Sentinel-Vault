# Changelog

## Unreleased

- `produce_video.py --list` prints a JSON catalog of script indexes and titles.
- `YouTubeAuditor.py --json` prints a combined channel/pipeline/stats report.
- YouTube auditor `--privacy {public,private,unlisted}` filters pipeline and stats rows.
- `health.py --format text` prints a key: value readiness report (JSON remains the default).
- Grader CLI `--format text` prints PASSED/FAILED verdicts (JSON file is still written).
- `python scripts/validate_scripts_json.py` checks video-factory scripts JSON against the ScriptEntry schema.
- `python scripts/validate_news_json.py` checks grader news JSON against the NewsItem schema.
- CLI `scripts/list_image_prompts.py` lists scene `image_prompt` values from scripts JSON.
- Open-source hygiene baseline: MIT LICENSE, EditorConfig, issue/PR templates,
  and README links to contributing, security, changelog, and license.
- `scripts/count_script_scenes.py` counts scenes in a scripts JSON file.
- `scripts/list_script_titles.py` lists `project_name` values from a scripts JSON file.
- `scripts/count_scripts.py` counts entries in a scripts JSON file.
- `scripts/total_narration_words.py` counts narration words in a scripts JSON file.

## 0.1.4

- Network-isolated pytest (`pytest-socket`) and coverage gate at 70%.
- Fresh-install verification script + CI job.
- Grader CLI `--input/--output`, optional news URLs, video `--dry-run`.
- Path sanitizer, rate limiter, auditor `--max-results`, health version env.
- Terraform module split (versions/variables/outputs) + plan in CI.

## 0.1.3

- Public-safe baseline: orphan history with no secret-bearing commits.
- Add SECURITY.md; scrub TOOLS.md and `.env.example` of any key material.
- Document hard rule: no hardcoded secrets on this public repository.

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
