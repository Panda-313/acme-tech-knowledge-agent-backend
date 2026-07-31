# Security Basics for Everyone

Last reviewed: May 2026

## Passwords & Authentication

- Use **1Password** for all work accounts. Do not reuse passwords.
- Enable hardware security keys (YubiKey) or passkeys wherever available.
- Never share your password or 2FA codes – not even with IT.
- Company SSO is the preferred way to log in to internal tools.

## Secrets Management

- **Never** commit secrets to Git (API keys, tokens, passwords, certificates).
- Use environment variables or the company secrets manager.
- If you accidentally commit a secret:
  1. Rotate it immediately
  2. Notify `#security`
  3. Remove it from history if possible (git filter-repo / BFG)

## Code & Data Handling

- Do not download production customer data to your laptop unless explicitly approved.
- When working with real data, prefer anonymized or synthetic datasets.
- Production database access is read-only by default and requires justification.

## Dependencies

- Run `npm audit` / `pip-audit` regularly.
- Prefer well-maintained libraries with recent releases.
- New dependencies that handle authentication, cryptography, or network traffic need extra review.

## AI Tools (reminder)

- Never paste production secrets, customer PII, or internal credentials into public AI models.
- Prefer local models or company-provisioned endpoints for sensitive work.

## Reporting Security Issues

- Suspected vulnerability or incident → post in `#security` or email security@acmetech.example
- We follow a blameless culture. Reporting early is always rewarded.

## Useful Links

- Internal security checklist (Drive)
- Security Champions program (ask in `#security`)

When in doubt, ask. It is always better to check than to assume.
