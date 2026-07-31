# Code Review Policy

Effective: January 2026

## Goals

- Catch bugs and design issues early
- Share knowledge across the team
- Keep the codebase maintainable and consistent
- Avoid blocking velocity with unnecessary bureaucracy

## Required Approvals

| Change Type                    | Required Approvals | Who can approve |
|--------------------------------|--------------------|-----------------|
| Regular feature / bugfix       | 1                  | Any senior or tech lead |
| Changes to auth, payments, security | 2             | At least one tech lead |
| Database migrations            | 1 + DBA review     | Tech lead + designated reviewer |
| AI / RAG pipeline changes      | 1                  | AI team member preferred |
| Documentation only             | 0 (self-merge OK)  | — |

## Pull Request Guidelines

### Before Opening a PR
- [ ] Code builds and tests pass locally
- [ ] You have self-reviewed the diff
- [ ] PR description explains *why*, not only *what*
- [ ] Linked Linear ticket (if applicable)
- [ ] Screenshots / recordings for UI changes

### PR Size
- Prefer PRs under **400 lines** of meaningful code change.
- Larger changes should be split into stacked PRs when possible.

### Review Turnaround
- Reviewers should respond within **1 business day**.
- If blocked, leave a comment and move on — do not leave PRs in limbo.

## What Reviewers Should Look For

1. **Correctness** – Does it do what it claims?
2. **Readability** – Will someone understand this in 6 months?
3. **Tests** – Are the important paths covered?
4. **Security** – Any secrets, injection risks, or over-permissioned code?
5. **Performance** – Obvious N+1 queries or large payloads?
6. **Consistency** – Follows existing patterns in the codebase?

## Approval & Merge

- Use GitHub "Approve" or "Request changes".
- Once approved, the author merges (or the reviewer if the author is unavailable).
- Squash merge is the default. Rebase only when history must stay linear.

## Hotfixes

For production incidents:
- Create a branch from `main`
- Get at least one approval (can be async via Slack in extreme cases)
- Merge and deploy immediately
- Follow up with a proper post-mortem ticket

## Exceptions

Tech leads may grant temporary exceptions for urgent customer work. Document the exception in the PR description.
