#!/usr/bin/env bash
# Verify a fresh clone can install from committed lockfiles and pass tests.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

echo "==> Fresh install workspace: $WORK"
cp -a "$ROOT/." "$WORK/repo"
cd "$WORK/repo"
rm -rf .venv .pytest_cache .mypy_cache .ruff_cache __pycache__ .git

python3 -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.lock
pip install -r requirements-dev.txt

echo "==> Running pytest"
pytest -q --disable-socket --allow-hosts=127.0.0.1
echo "==> Fresh install OK"
