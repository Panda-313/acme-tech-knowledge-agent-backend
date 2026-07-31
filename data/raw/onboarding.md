# AcmeTech Onboarding Guide

Welcome to AcmeTech! We're building the next generation of Angular + AI applications. This guide will help you get productive in your first two weeks.

## Your First Day

1. **Accounts & Access**
   - Slack (company workspace) – join `#general`, `#engineering`, `#ai-experiments`
   - GitHub Enterprise – request access via IT ticket
   - 1Password – company vault will be shared with you
   - Google Workspace – calendar, Drive, email
   - Linear – project management (invite will be sent by your manager)

2. **Hardware**
   - MacBook Pro M-series (or Linux workstation if preferred)
   - External monitor and docking station available on request

3. **Required Reading (Day 1)**
   - `tech-stack.md`
   - `security-basics.md`
   - `ai-usage-guidelines.md`
   - Company values (shared in Drive)

## Week 1 Checklist

- [ ] Set up local development environment (see `tech-stack.md`)
- [ ] Complete security training (30 min, link in Slack)
- [ ] Pair with a buddy on a small ticket
- [ ] Attend the weekly Engineering Sync (Tuesday 10:00)
- [ ] Introduce yourself in `#engineering` with a short note about your background

## Development Setup

```bash
# Clone the main monorepo
git clone git@github.com:acmetech/platform.git
cd platform

# Install dependencies
npm install          # frontend
pip install -r requirements.txt  # backend

# Start local services
docker compose up -d   # Postgres, Redis, Chroma
```

Full setup instructions are in the `README.md` of the platform repo.

## Culture & Communication

- We value **ownership** and **direct feedback**.
- Default to async communication (Linear comments, Slack threads).
- Meetings have agendas and notes. If a meeting has no agenda, you can decline.
- We ship small, frequently. Prefer PRs under 400 lines when possible.

## People to Know

| Role              | Name          | Slack handle   |
|-------------------|---------------|----------------|
| Engineering Manager | Anna Kowalska | @anna          |
| Tech Lead (Frontend) | Marek Nowak | @marek         |
| Tech Lead (AI)    | Sofia Rivera  | @sofia         |
| People Ops        | Tom Ellis     | @tom           |

## Questions?

Ask in `#onboarding` or message your manager. There are no stupid questions in the first month.

Welcome aboard – we're glad you're here.
