# Performance Guidelines

## Frontend (Angular)

### Budgets (enforced in CI where possible)

| Metric                        | Target          | Hard Limit |
|-------------------------------|-----------------|------------|
| Initial bundle (main)         | < 200 KB gzip   | 300 KB     |
| Largest Contentful Paint      | < 2.0 s         | 2.5 s      |
| Time to Interactive           | < 3.0 s         | 3.5 s      |
| Cumulative Layout Shift       | < 0.1           | 0.15       |

### Best Practices

- Prefer Signals and `OnPush` (or the new signal-based components)
- Lazy-load routes and heavy libraries
- Avoid large third-party packages when a lighter alternative exists
- Use `trackBy` (or the new control-flow equivalents) in lists
- Images: modern formats (WebP/AVIF), proper sizing, lazy loading
- Measure with Lighthouse and the Angular DevTools profiler

## Backend (FastAPI / Python)

### Targets

- p95 latency for simple read endpoints: < 100 ms
- p95 latency for complex endpoints (including RAG): < 1.5 s
- Error rate: < 0.1 % under normal load

### Best Practices

- Use async endpoints and async database drivers where it matters
- Avoid N+1 queries – use `selectinload` / `joinedload` or explicit joins
- Cache expensive or frequently accessed data in Redis with clear TTLs
- Paginate list endpoints by default
- Set sensible timeouts on external calls (LLM providers especially)

## RAG / AI Specific

- Keep retrieved context under a reasonable token budget (monitor cost and latency)
- Cache embeddings of static documents
- Prefer smaller, faster models for classification / routing; reserve larger models for final generation
- Always measure end-to-end latency (retrieval + generation)

## Monitoring

- Frontend: Real User Monitoring (in progress) + Lighthouse CI
- Backend: OpenTelemetry traces + Prometheus metrics
- AI: token usage, retrieval latency, answer latency, evaluation scores

## When Performance Becomes a Feature

If a change significantly improves (or degrades) one of the key metrics above, mention it in the PR description and consider adding a note to the relevant team channel.
