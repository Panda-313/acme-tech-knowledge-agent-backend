# Standardy projektowania API

## Zasady ogólne

- RESTful tam, gdzie pasuje; pragmatycznie tam, gdzie nie pasuje
- Spójne nazewnictwo i kształt odpowiedzi
- Jawne wersjonowanie
- Czytelne komunikaty błędów pomocne dla klienta

## Struktura URL

```
https://api.acmetech.example/v1/resources
https://api.acmetech.example/v1/resources/{id}
https://api.acmetech.example/v1/resources/{id}/sub-resources
```

- Używaj kebab-case dla wielowyrazowych segmentów ścieżki
- Dla kolekcji preferuj rzeczowniki w liczbie mnogiej
- Wersję podawaj w ścieżce (`/v1/`, `/v2/`)

## Metody HTTP

| Metoda | Zastosowanie                       |
|--------|------------------------------------|
| GET    | Odczyt (safe, idempotent)          |
| POST   | Tworzenie lub akcje nieidempotentne |
| PUT    | Pełne nadpisanie                   |
| PATCH  | Częściowa aktualizacja             |
| DELETE | Usunięcie                          |

## Request i response

- Tylko JSON (chyba że streaming lub pobieranie pliku)
- Ciała requestów walidowane modelami Pydantic
- Odpowiedzi sukcesu: odpowiedni status 2xx + body JSON
- Kolekcje powinny wspierać paginację (`limit`, `cursor` albo `offset`)

### Standardowa koperta sukcesu (opcjonalna, ale rekomendowana dla nowych endpointów)

```json
{
  "data": { ... },
  "meta": {
    "request_id": "..."
  }
}
```

### Odpowiedź błędu

```json
{
  "error": {
    "code": "validation_error",
    "message": "Czytelny komunikat",
    "details": [ ... ]
  },
  "meta": {
    "request_id": "..."
  }
}
```

Używaj spójnych kodów błędów między usługami.

## Uwierzytelnianie

- Bearer token (JWT lub opaque) w nagłówku `Authorization`
- Service-to-service: mTLS albo podpisane tokeny wewnętrzne (szczegóły w dokumentacji security)

## Paginacja

Dla dużych lub często zmieniających się kolekcji preferuj paginację opartą o cursor:

```
GET /v1/items?limit=20&cursor=eyJ...
```

## Streaming

Dla odpowiedzi LLM używamy Server-Sent Events (SSE) lub chunked transfer encoding.  
Dokumentuj dokładny format w docstringu endpointu.

## Dokumentacja

- Każdy publiczny endpoint musi mieć wpis OpenAPI (FastAPI obsługuje większość automatycznie)
- Utrzymuj opisy endpointów aktualne
- Zmiany breaking wymagają nowej wersji major i przewodnika migracji

## Deprecacja

- Deprecacje zewnętrznych API ogłaszaj co najmniej 90 dni wcześniej
- Wewnętrzne API mogą zmieniać się szybciej, ale nadal wymagają komunikacji na `#engineering`
