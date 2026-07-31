# FAQ for Developers

Quick answers to questions that come up often. If something is missing, add it via PR.

## General

**Q: Where is the main codebase?**  
A: `github.com/acmetech/platform` (monorepo). Frontend lives under `/apps/web`, backend under `/services`.

**Q: How do I get access to production logs?**  
A: Ask in `#devops`. Access is granted via AWS SSO after approval.

**Q: What is the preferred branch naming?**  
A: `feat/short-description`, `fix/ticket-123`, `chore/...`. Include the Linear ticket ID when possible.

## Local Development

**Q: Docker is eating all my RAM. What can I do?**  
A: Use `docker compose up` only for the services you need. Many people run Postgres and Redis natively and only containerize the rest.

**Q: How do I reset the local database?**  
A: `make db-reset` (or `alembic downgrade base && alembic upgrade head` + seed script).

**Q: Frontend hot reload is slow.**  
A: Make sure you are on the latest Angular CLI and using the esbuild builder. Also try disabling source maps temporarily.

## AI / RAG Related

**Q: Can I use company documents in public ChatGPT?**  
A: No. See `ai-usage-guidelines.md`. Use local models or company-approved endpoints.

**Q: How do I test the Knowledge Bot locally?**  
A: Follow the README in `/services/knowledge-bot`. You need ChromaDB running and the markdown docs indexed.

**Q: Which embedding model should I use for experiments?**  
A: Start with `all-MiniLM-L6-v2` (local, fast, free). Switch to OpenAI embeddings only when you need higher quality and have budget approval.

## Process

**Q: Do I need a Linear ticket for every PR?**  
A: For anything larger than a typo or tiny fix – yes. It helps with prioritization and later auditing.

**Q: Who decides on new libraries?**  
A: Tech leads + a short discussion in `#engineering`. We prefer not to add dependencies lightly.

**Q: How often do we deploy?**  
A: Backend services: multiple times per day. Frontend: continuous on merge to `main` (with feature flags when needed).

## Still stuck?

Ask in `#engineering` or the relevant team channel. Someone will help.
