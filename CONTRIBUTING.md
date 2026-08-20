# Keep this short. Prefer issues + focused PRs with tests.

## Workflow

1. Create a branch from `main`.
2. Make one logical change (feature or fix) with tests that pin the behavior.
3. Run `pytest -q` and `ruff check .` locally.
4. Open a PR; CI must be green.

## Commit style

- One concern per commit when practical.
- Include tests in the same commit as the behavior they prove.
- Do not commit secrets, tokens, or machine-specific absolute paths.
