# Przegląd architektury

Widok wysokiego poziomu platformy AcmeTech (stan na połowę 2026 roku).

## Kontekst systemu

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Angular    │────▶│  API Gateway /   │────▶│  Mikrousługi    │
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

## Główne komponenty

### Frontend (Angular)
- Aplikacja Single Page Application
- Komunikuje się z warstwą Backend-for-Frontend (BFF)
- Używa Signals dla większości stanu lokalnego, NgRx tylko dla złożonego stanu współdzielonego
- Uwierzytelnianie przez OIDC (Authorization Code + PKCE)

### Usługi backendowe
- **API Gateway / BFF** – aplikacja FastAPI agregująca wywołania i obsługująca auth
- **Core Services** – zarządzanie użytkownikami, billing, ustawienia projektów
- **Knowledge Service** – pipeline RAG, indeksacja dokumentów, endpointy czatu
- **Worker** – workery Celery do zadań długotrwałych (indeksacja, ewaluacje, raporty)

### Magazyny danych
- **PostgreSQL** – źródło prawdy dla danych biznesowych
- **Redis** – cache, rate limiting, broker dla Celery
- **Vector Store** – ChromaDB (development) / Qdrant (production) dla embeddingów

### Pipeline AI (Knowledge Bot)
1. Dokumenty (Markdown) są dzielone na chunki
2. Generowane są embeddingi (lokalnie lub przez OpenAI)
3. Embeddingi trafiają do bazy wektorowej wraz z metadanymi (plik źródłowy, sekcja itd.)
4. W czasie zapytania: embedding pytania → pobranie top-k chunków → budowa promptu → wywołanie LLM → odpowiedź + źródła

## Środowiska

| Środowisko | Cel                        | Dane          |
|------------|----------------------------|---------------|
| local      | Komputery developerów      | Syntetyczne   |
| staging    | Testy przedprodukcyjne     | Anonimizowane |
| production | Klienci i użytkownicy wewnętrzni | Rzeczywiste |

## Kluczowe zasady projektowe

- **Async by default** w usługach Python
- **Explicit over magic** – czytelne granice między usługami
- **Observability** – każde żądanie powinno być możliwe do prześledzenia (OpenTelemetry w toku)
- **Fail safely** – funkcje AI degradowane łagodnie, gdy model jest niedostępny

Więcej szczegółów znajdziesz w README poszczególnych usług i ADR-ach w `/docs/adr`.
