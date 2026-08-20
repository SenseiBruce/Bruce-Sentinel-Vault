# Security Policy

## No secrets in this repository

This is a **public** project. Do not commit:

- API keys, bearer tokens, passwords, or OAuth client secrets
- `.env` files or `*_token.json`
- Private infrastructure details (SSH keys, internal IPs)

Use `.env.example` for variable **names** only. Real values stay in a local
gitignored `.env`.

## Reporting a leak

1. Rotate the exposed credential with the provider immediately.
2. Open an issue (without pasting the secret) or email the maintainer.
3. We will scrub history and force-push if needed.

## Automated guards

- `.gitignore` excludes `.env` and token files
- `pre-commit` + CI run **gitleaks** on every push
- Dependabot updates dependencies weekly
