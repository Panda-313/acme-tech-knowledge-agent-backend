# Obsługa incydentów

## Poziomy ważności

| Poziom | Opis                                             | Czas reakcji    | Przykład |
|--------|--------------------------------------------------|-----------------|----------|
| SEV-1  | Całkowita niedostępność lub ryzyko utraty danych | Natychmiast     | Auth down, niedziałające płatności |
| SEV-2  | Kluczowa funkcja niedostępna dla wielu użytkowników | < 30 min     | Knowledge Bot całkowicie niedostępny |
| SEV-3  | Spadek wydajności lub częściowa awaria funkcji   | < 2 godziny     | Wysokie opóźnienia, część retrievalu nie działa |
| SEV-4  | Problem drobny, istnieje obejście                | Następny dzień roboczy | Błąd kosmetyczny, niekrytyczne ostrzeżenie |

## Jak zgłosić incydent

1. Napisz na `#incidents` z poziomem SEV i krótkim opisem
2. Jeśli to SEV-1 lub SEV-2, wezwij też inżyniera on-call (PagerDuty)
3. Utwórz ticket w Linear z etykietą `incident` oraz poziomem SEV

## Role podczas incydentu

- **Incident Commander** – koordynuje działania, decyduje o komunikacji, pilnuje osi czasu
- **Technical Lead** – prowadzi analizę i dowozi naprawę
- **Communications** – aktualizuje status page / interesariuszy wewnętrznych (w mniejszych incydentach często ta sama osoba)

W większości incydentów jedna osoba pełni kilka ról naraz.

## Oczekiwania komunikacyjne

- Podczas aktywnego SEV-1/2 aktualizuj `#incidents` co najmniej co 30 minut
- Przy wpływie na klientów aktualizuj zewnętrzną status page
- Po rozwiązaniu incydentu opublikuj krótkie podsumowanie

## Po incydencie

1. W ciągu 48 godzin: przygotuj blameless post-mortem w Linear lub Notion
2. Zidentyfikuj action itemy z właścicielami i terminami
3. Udostępnij post-mortem na `#engineering`
4. Śledź realizację action itemów do końca

## Przydatne komendy i linki

- Status page: status.acmetech.example
- PagerDuty: (link w 1Password)
- Runbooki: `/docs/runbooks` w repo platformy

## Pamiętaj

Stosujemy **blameless** przeglądy incydentów. Celem jest nauka i poprawa systemu, a nie szukanie winnych.
