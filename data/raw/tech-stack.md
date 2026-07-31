# AcmeTech Technology Stack

Last updated: July 2026

## Overview

AcmeTech builds internal and customer-facing tools using a modern Angular + Python stack with a strong focus on AI-assisted development and RAG-based knowledge systems.

## Frontend

| Layer              | Technology                          | Notes |
|--------------------|-------------------------------------|-------|
| Framework          | Angular 19                          | Standalone components, Signals |
| UI Library         | Angular Material + Tailwind CSS     | Custom design system on top |
| State Management   | NgRx Signal Store / Signals         | Prefer Signals for new code |
| HTTP               | HttpClient + interceptors           | Auth + error handling |
| Testing            | Jest + Angular Testing Library      | Unit + component tests |
| E2E                | Playwright                          | Critical user flows |
| Build              | Angular CLI + esbuild               | |

### Frontend Conventions
- Strict TypeScript (`strict: true`)
- Prefer standalone components
- Use `input()` / `output()` functions (not decorators)
- All new features must have at least basic unit tests

## Backend

| Layer              | Technology                          | Notes |
|--------------------|-------------------------------------|-------|
| Language           | Python 3.12                         | |
| Framework          | FastAPI                             | Async preferred |
| ORM                | SQLAlchemy 2.0 + Alembic            | |
| Database           | PostgreSQL 16                       | Primary data store |
| Cache / Queue      | Redis                               | Sessions, Celery |
| Validation         | Pydantic v2                         | |
| Testing            | pytest + httpx                      | |

## AI / LLM Layer

| Component          | Technology                          | Notes |
|--------------------|-------------------------------------|-------|
| Orchestration      | LangChain / LlamaIndex              | Currently evaluating both |
| Vector Store       | ChromaDB (local) → Qdrant (prod)    | |
| Embeddings         | `sentence-transformers/all-MiniLM-L6-v2` or OpenAI `text-embedding-3-small` | Local preferred for cost |
| LLM Providers      | Groq (primary), Ollama (local), OpenAI (fallback) | |
| RAG Evaluation     | Custom + Ragas                      | |

## Infrastructure & DevOps

- **Containers**: Docker + Docker Compose (local)
- **CI/CD**: GitHub Actions
- **Hosting**: Currently AWS (ECS + RDS). Migration to Railway / Fly.io under evaluation for smaller services.
- **Secrets**: 1Password + AWS Secrets Manager
- **Monitoring**: OpenTelemetry + Grafana (in progress)

## Local Development Requirements

- Node.js 22+
- Python 3.12+
- Docker Desktop / Colima
- Git

## Version Policy

- We stay on the latest LTS / stable versions.
- Major upgrades are planned quarterly and announced in `#engineering`.
