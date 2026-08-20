# Security Policy

## No secrets in this repository

This is a **public** project. Do not commit:

- API keys, bearer tokens, passwords, or OAuth client secrets
- `.env` files or `*_token.json`
- Private infrastructure details (SSH keys, internal IPs)

Use `.env.example` for variable **names** only. Real values stay in a local
gitignored `.env`.

## If credentials were ever committed

Force-pushing rewritten history removes secrets from branch tips, but **GitHub may
still serve old commit SHAs** that were referenced by pull requests or forks.

1. **Rotate every exposed key immediately** with the provider (treat it as burned).
2. Optionally ask GitHub Support to purge unreachable commits, or recreate the
   repository if you need the old SHAs gone from `api.github.com` as well.


## Automated guards

- `.gitignore` excludes `.env` and token files
- `pre-commit` + CI run **gitleaks** on every push
- Dependabot updates dependencies weekly
