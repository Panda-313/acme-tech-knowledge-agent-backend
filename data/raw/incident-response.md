# Incident Response

## Severity Levels

| Severity | Description                                      | Response Time | Example |
|----------|--------------------------------------------------|---------------|---------|
| SEV-1    | Complete outage or data loss risk                | Immediate     | Auth down, payment processing broken |
| SEV-2    | Major feature unavailable for many users         | < 30 min      | Knowledge Bot completely down |
| SEV-3    | Degraded performance or partial feature failure  | < 2 hours     | High latency, some retrieval failures |
| SEV-4    | Minor issue, workaround exists                   | Next business day | Cosmetic bug, non-critical warning |

## How to Declare an Incident

1. Post in `#incidents` with the severity and a short description
2. If SEV-1 or SEV-2, also page the on-call engineer (PagerDuty)
3. Create a Linear ticket with label `incident` and the severity

## Roles During an Incident

- **Incident Commander** – coordinates, decides on communication, keeps timeline
- **Technical Lead** – investigates and drives the fix
- **Communications** – updates status page / internal stakeholders (often the same person for smaller incidents)

For most incidents one person wears multiple hats.

## Communication Expectations

- Update `#incidents` at least every 30 minutes during active SEV-1/2
- External status page is updated for customer-facing impact
- After resolution, a short summary is posted

## Post-Incident

1. Within 48 hours: write a blameless post-mortem in Linear or Notion
2. Identify action items with owners and due dates
3. Share the post-mortem in `#engineering`
4. Track action items to completion

## Useful Commands & Links

- Status page: status.acmetech.example
- PagerDuty: (link in 1Password)
- Runbooks: `/docs/runbooks` in the platform repo

## Remember

We practice **blameless** incident reviews. The goal is learning and system improvement, not finding who to blame.
