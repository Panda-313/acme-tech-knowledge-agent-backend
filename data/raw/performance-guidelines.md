# Wytyczne wydajnościowe

## Frontend (Angular)

### Budżety (egzekwowane w CI tam, gdzie to możliwe)

| Metryka                       | Cel             | Twardy limit |
|-------------------------------|-----------------|--------------|
| Initial bundle (main)         | < 200 KB gzip   | 300 KB       |
| Largest Contentful Paint      | < 2.0 s         | 2.5 s        |
| Time to Interactive           | < 3.0 s         | 3.5 s        |
| Cumulative Layout Shift       | < 0.1           | 0.15         |

### Dobre praktyki

- Preferuj Signals i `OnPush` (albo nowe komponenty oparte o sygnały)
- Stosuj lazy loading dla tras i ciężkich bibliotek
- Unikaj dużych paczek third-party, jeśli istnieje lżejsza alternatywa
- Używaj `trackBy` (lub odpowiedników w nowym control-flow) na listach
- Obrazy: nowoczesne formaty (WebP/AVIF), poprawne rozmiary, lazy loading
- Mierz przez Lighthouse i profiler Angular DevTools

## Backend (FastAPI / Python)

### Cele

- Opóźnienie p95 dla prostych endpointów odczytowych: < 100 ms
- Opóźnienie p95 dla endpointów złożonych (w tym RAG): < 1.5 s
- Error rate: < 0.1% przy normalnym obciążeniu

### Dobre praktyki

- Używaj endpointów async i asynchronicznych driverów bazy tam, gdzie to istotne
- Unikaj zapytań N+1 — stosuj `selectinload` / `joinedload` albo jawne joiny
- Cache’uj kosztowne lub często używane dane w Redisie z jasno określonym TTL
- Domyślnie paginuj endpointy listujące
- Ustaw sensowne timeouty dla wywołań zewnętrznych (szczególnie do dostawców LLM)

## RAG / AI

- Utrzymuj kontekst z retrievalu w rozsądnym budżecie tokenów (monitoruj koszt i opóźnienie)
- Cache’uj embeddingi statycznych dokumentów
- Do klasyfikacji / routingu preferuj mniejsze i szybsze modele; większe rezerwuj do końcowej generacji
- Zawsze mierz opóźnienie end-to-end (retrieval + generation)

## Monitoring

- Frontend: Real User Monitoring (w toku) + Lighthouse CI
- Backend: trace’y OpenTelemetry + metryki Prometheus
- AI: zużycie tokenów, opóźnienie retrievalu, opóźnienie odpowiedzi, wyniki ewaluacji

## Gdy wydajność staje się funkcją

Jeśli zmiana istotnie poprawia (lub pogarsza) jedną z kluczowych metryk powyżej, opisz to w PR i rozważ notkę na odpowiednim kanale zespołu.
