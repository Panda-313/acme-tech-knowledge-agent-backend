# Deployment Process

## Overview

We practice continuous deployment for most services. Merging to `main` triggers the pipeline.

## Environments & Promotion

```
feature branch → PR → main → staging (auto) → production (manual approval for critical services)
```

- **Staging** is automatically updated on every merge to `main`.
- **Production** deployments for the Knowledge Service and billing-related services require a manual approval step in GitHub Actions.
- Frontend is deployed continuously with feature flags when risk is higher.

## Pipeline Steps (simplified)

1. Lint & type-check
2. Unit + integration tests
3. Build Docker images
4. Push to container registry
5. Deploy to staging
6. Smoke tests on staging
7. (Optional) Manual approval
8. Deploy to production
9. Post-deploy health checks

## Feature Flags

We use a simple internal feature-flag service (and LaunchDarkly for some customer-facing flags).  
Large or risky changes should be behind a flag so they can be turned off without a rollback.

## Database Migrations

- Migrations are written with Alembic.
- They run automatically as part of the deployment job **before** the new application version starts.
- Breaking changes (column drops, renames) must be done in two phases (expand → contract) and coordinated with the team.

## Rollbacks

- Application rollback: re-deploy the previous image tag (one click in the GitHub Actions UI or via CLI).
- Database rollback: only possible if the migration was reversible and no data loss occurred. Prefer forward fixes.

## Hotfixes

1. Branch from `main`
2. Fix + tests
3. Fast-track review (1 approval minimum)
4. Merge and deploy
5. Write a short incident note in Linear

## Monitoring After Deploy

- Watch the `#deploys` Slack channel
- Check Grafana dashboards for error rate, latency, and saturation
- AI services: also monitor token usage and retrieval quality metrics

## Who Can Deploy?

- Any engineer can merge to `main` (after review).
- Production approvals for critical paths are limited to tech leads and on-call engineers.
