# Architecture Overview

High-level view of the AcmeTech platform (as of mid-2026).

## System Context

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Angular    │────▶│  API Gateway /   │────▶│  Microservices  │
│  Frontend   │     │  FastAPI BFF     │     │  (Python)       │
└─────────────┘     └──────────────────┘     └────────┬────────┘
                                                      │
                       ┌──────────────────────────────┼──────────────────────────────┐
                       ▼                              ▼                              ▼
                ┌─────────────┐               ┌─────────────┐               ┌─────────────┐
                │ PostgreSQL  │               │    Redis    │               │  ChromaDB / │
                │             │               │             │               │   Qdrant    │
                └─────────────┘               └─────────────┘               └─────────────┘
```

## Main Components

### Frontend (Angular)
- Single Page Application
- Communicates with a Backend-for-Frontend (BFF) layer
- Uses Signals for most local state, NgRx only for complex shared state
- Authentication via OIDC (Authorization Code + PKCE)

### Backend Services
- **API Gateway / BFF** – FastAPI application that aggregates calls and handles auth
- **Core Services** – user management, billing, project settings
- **Knowledge Service** – RAG pipeline, document indexing, chat endpoints
- **Worker** – Celery workers for long-running tasks (indexing, evaluations, reports)

### Data Stores
- **PostgreSQL** – source of truth for business data
- **Redis** – caching, rate limiting, Celery broker
- **Vector Store** – ChromaDB (development) / Qdrant (production) for embeddings

### AI Pipeline (Knowledge Bot)
1. Documents (Markdown) are chunked
2. Embeddings generated (local or OpenAI)
3. Stored in vector database with metadata (source file, section, etc.)
4. At query time: embed question → retrieve top-k chunks → build prompt → call LLM → return answer + sources

## Environments

| Environment | Purpose                    | Data          |
|-------------|----------------------------|---------------|
| local       | Developer machines         | Synthetic     |
| staging     | Pre-production testing     | Anonymized    |
| production  | Live customers & internal  | Real          |

## Key Design Principles

- **Async by default** in Python services
- **Explicit over magic** – clear boundaries between services
- **Observability** – every request should be traceable (OpenTelemetry in progress)
- **Fail safely** – AI features degrade gracefully when the model is unavailable

For deeper details see individual service READMEs and the ADRs in `/docs/adr`.
