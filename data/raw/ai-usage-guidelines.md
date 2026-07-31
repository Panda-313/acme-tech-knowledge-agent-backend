# AI Usage Guidelines at AcmeTech

Last updated: June 2026

## Purpose

These guidelines help us use AI tools productively while protecting company data, customer privacy, and code quality.

## Allowed Tools

| Tool                    | Allowed | Notes |
|-------------------------|---------|-------|
| GitHub Copilot          | ✅      | Company license |
| Cursor / Windsurf       | ✅      | With company account |
| ChatGPT / Claude (web)  | ✅      | Do **not** paste secrets or customer data |
| Groq / OpenAI API       | ✅      | Use company keys only |
| Local models (Ollama)   | ✅      | Preferred for sensitive code |
| Public free tools       | ⚠️      | Only for non-sensitive, non-proprietary content |

## Golden Rules

1. **Never paste secrets, API keys, passwords, or customer PII** into any external AI tool.
2. **Never commit AI-generated code without reviewing it.** You own every line that lands in `main`.
3. Prefer **local models** (Ollama) or company-approved APIs when working with internal documents or customer data.
4. AI is a **pair programmer**, not an author. You must understand the code you submit.
5. When using AI for architecture or design decisions, document the reasoning in the PR or Linear ticket.

## What Is Encouraged

- Generating boilerplate, tests, and documentation drafts
- Explaining unfamiliar code or error messages
- Brainstorming alternative implementations
- Writing commit messages and PR descriptions
- Creating synthetic test data
- Building internal RAG prototypes (like this Knowledge Bot)

## What Is Discouraged / Forbidden

- Submitting large AI-generated PRs without meaningful human review
- Using public AI tools with production database schemas or real customer data
- Generating code that bypasses our security or authentication patterns
- Relying on AI for final architectural decisions without team discussion

## RAG & Internal Knowledge

We are actively building internal RAG systems (see Knowledge Bot initiative).  
When contributing to these systems:

- Only index documents that are already approved for internal distribution
- Do not index customer data or personal employee information unless explicitly approved by Legal/People Ops
- Always show sources in answers when the system supports it

## Reporting Issues

If you discover that sensitive data was accidentally sent to an external model, notify `#security` immediately.

Questions about these guidelines → ask in `#ai-experiments` or message Sofia (@sofia).
