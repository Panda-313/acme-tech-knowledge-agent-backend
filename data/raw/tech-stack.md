# Stos technologiczny AcmeTech

Ostatnia aktualizacja: lipiec 2026

## Przegląd

AcmeTech buduje narzędzia wewnętrzne i klienckie w nowoczesnym stacku Angular + Python, z mocnym naciskiem na development wspierany AI oraz systemy wiedzy oparte o RAG.

## Frontend

| Warstwa            | Technologia                         | Uwagi |
|--------------------|-------------------------------------|-------|
| Framework          | Angular 19                          | Standalone components, Signals |
| Biblioteka UI      | Angular Material + Tailwind CSS     | Nad tym działa własny design system |
| Zarządzanie stanem | NgRx Signal Store / Signals         | Dla nowego kodu preferujemy Signals |
| HTTP               | HttpClient + interceptory           | Auth + obsługa błędów |
| Testy              | Jest + Angular Testing Library      | Testy unit i komponentowe |
| E2E                | Playwright                          | Krytyczne ścieżki użytkownika |
| Build              | Angular CLI + esbuild               | |

### Konwencje frontendowe
- Ścisły TypeScript (`strict: true`)
- Preferuj standalone components
- Używaj funkcji `input()` / `output()` (zamiast dekoratorów)
- Każda nowa funkcja musi mieć co najmniej podstawowe testy unit

## Backend

| Warstwa            | Technologia                         | Uwagi |
|--------------------|-------------------------------------|-------|
| Język              | Python 3.12                         | |
| Framework          | FastAPI                             | Preferowane podejście async |
| ORM                | SQLAlchemy 2.0 + Alembic            | |
| Baza danych        | PostgreSQL 16                       | Główny magazyn danych |
| Cache / kolejka    | Redis                               | Sesje, Celery |
| Walidacja          | Pydantic v2                         | |
| Testy              | pytest + httpx                      | |

## Warstwa AI / LLM

| Komponent          | Technologia                         | Uwagi |
|--------------------|-------------------------------------|-------|
| Orkiestracja       | LangChain / LlamaIndex              | Aktualnie oceniamy oba podejścia |
| Vector Store       | ChromaDB (lokalnie) → Qdrant (prod) | |
| Embeddingi         | `sentence-transformers/all-MiniLM-L6-v2` lub OpenAI `text-embedding-3-small` | Lokalnie preferowane kosztowo |
| Dostawcy LLM       | Groq (główny), Ollama (lokalnie), OpenAI (fallback) | |
| Ewaluacja RAG      | Custom + Ragas                      | |

## Infrastruktura i DevOps

- **Kontenery**: Docker + Docker Compose (lokalnie)
- **CI/CD**: GitHub Actions
- **Hosting**: Aktualnie AWS (ECS + RDS). Dla mniejszych usług rozważamy migrację do Railway / Fly.io.
- **Sekrety**: 1Password + AWS Secrets Manager
- **Monitoring**: OpenTelemetry + Grafana (w toku)

## Wymagania do lokalnego developmentu

- Node.js 22+
- Python 3.12+
- Docker Desktop / Colima
- Git

## Polityka wersji

- Trzymamy się najnowszych stabilnych wersji / LTS.
- Duże aktualizacje planujemy kwartalnie i ogłaszamy na `#engineering`.
