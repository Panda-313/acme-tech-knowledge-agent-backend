# Proces deploymentu

## Przegląd

W większości usług stosujemy continuous deployment. Merge do `main` uruchamia pipeline.

## Środowiska i promocja zmian

```
feature branch → PR → main → staging (auto) → production (manual approval dla krytycznych usług)
```

- **Staging** aktualizuje się automatycznie po każdym merge do `main`.
- **Production** dla Knowledge Service i usług powiązanych z billingiem wymaga kroku manual approval w GitHub Actions.
- Frontend deployujemy ciągle, używając feature flag przy wyższym ryzyku.

## Kroki pipeline’u (uproszczone)

1. Lint i type-check
2. Testy unit i integracyjne
3. Build obrazów Dockera
4. Push do rejestru kontenerów
5. Deploy na staging
6. Smoke testy na staging
7. (Opcjonalnie) Manual approval
8. Deploy na production
9. Kontrole zdrowia po deployu

## Feature flagi

Używamy prostego wewnętrznego serwisu feature flag (a dla części funkcji klienckich także LaunchDarkly).  
Duże lub ryzykowne zmiany powinny być za flagą, żeby dało się je wyłączyć bez rollbacku.

## Migracje bazy danych

- Migracje piszemy w Alembic.
- Uruchamiają się automatycznie w jobie deploymentowym **przed** startem nowej wersji aplikacji.
- Zmiany breaking (usuwanie kolumn, zmiany nazw) robimy dwuetapowo (expand → contract) i koordynujemy z zespołem.

## Rollbacki

- Rollback aplikacji: redeploy poprzedniego taga obrazu (jednym kliknięciem w GitHub Actions UI lub przez CLI).
- Rollback bazy: możliwy tylko przy odwracalnej migracji i braku utraty danych. Preferujemy poprawki forward.

## Hotfixy

1. Utwórz branch od `main`
2. Wprowadź fix + testy
3. Szybki review (minimum 1 approval)
4. Merge i deploy
5. Dodaj krótką notatkę o incydencie w Linear

## Monitoring po deployu

- Obserwuj kanał Slack `#deploys`
- Sprawdzaj dashboardy Grafany pod kątem error rate, latency i saturation
- Dla usług AI monitoruj też zużycie tokenów i metryki jakości retrievalu

## Kto może deployować?

- Każdy inżynier może mergować do `main` (po review).
- Approvale produkcyjne dla krytycznych ścieżek są ograniczone do tech leadów i inżynierów on-call.
