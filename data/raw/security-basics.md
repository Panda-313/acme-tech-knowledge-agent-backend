# Podstawy bezpieczeństwa dla wszystkich

Ostatni przegląd: maj 2026

## Hasła i uwierzytelnianie

- Używaj **1Password** do wszystkich kont służbowych. Nie używaj tych samych haseł ponownie.
- Włącz sprzętowe klucze bezpieczeństwa (YubiKey) lub passkeys tam, gdzie to dostępne.
- Nigdy nie udostępniaj hasła ani kodów 2FA — nawet działowi IT.
- Firmowe SSO to preferowany sposób logowania do narzędzi wewnętrznych.

## Zarządzanie sekretami

- **Nigdy** nie commituj sekretów do Gita (API key, tokeny, hasła, certyfikaty).
- Używaj zmiennych środowiskowych lub firmowego menedżera sekretów.
- Jeśli przypadkowo zacommitujesz sekret:
  1. Natychmiast go zrotuj
  2. Powiadom `#security`
  3. Usuń go z historii, jeśli to możliwe (git filter-repo / BFG)

## Obsługa kodu i danych

- Nie pobieraj produkcyjnych danych klientów na laptopa bez wyraźnej zgody.
- Przy pracy na realnych danych preferuj zbiory zanonimizowane lub syntetyczne.
- Dostęp do produkcyjnej bazy domyślnie jest tylko do odczytu i wymaga uzasadnienia.

## Zależności

- Uruchamiaj regularnie `npm audit` / `pip-audit`.
- Preferuj biblioteki dobrze utrzymywane i regularnie aktualizowane.
- Nowe zależności obsługujące auth, kryptografię lub ruch sieciowy wymagają dodatkowego przeglądu.

## Narzędzia AI (przypomnienie)

- Nigdy nie wklejaj sekretów produkcyjnych, PII klientów ani wewnętrznych danych uwierzytelniających do publicznych modeli AI.
- Do wrażliwej pracy preferuj modele lokalne lub firmowe endpointy.

## Zgłaszanie problemów bezpieczeństwa

- Podejrzenie podatności lub incydentu → napisz na `#security` albo wyślij email na security@acmetech.example
- Pracujemy w kulturze blameless. Wczesne zgłoszenia są zawsze mile widziane.

## Przydatne linki

- Wewnętrzna checklista bezpieczeństwa (Drive)
- Program Security Champions (zapytaj na `#security`)

Gdy masz wątpliwości — zapytaj. Lepiej sprawdzić niż zakładać.
