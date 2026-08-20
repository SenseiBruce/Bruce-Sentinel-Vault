# TOOLS.md - Local Notes (public-safe)

This public repository must never store API keys, tokens, passwords, or
machine-specific secrets.

## Allowed here

- Non-sensitive tool preferences (voice names, workflow notes)
- Links to public docs

## Not allowed here

- API keys / bearer tokens
- `.env` contents
- OAuth token JSON
- Private hostnames, IPs, or SSH credentials

Put secrets only in a local `.env` (gitignored). Copy from `.env.example`.
