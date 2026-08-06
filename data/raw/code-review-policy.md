# Polityka code review

Obowiązuje od: styczeń 2026

## Cele

- Wczesne wykrywanie błędów i problemów projektowych
- Dzielenie się wiedzą w zespole
- Utrzymanie kodu w stanie spójnym i łatwym do rozwijania
- Unikanie blokowania velocity przez zbędną biurokrację

## Wymagane approvale

| Typ zmiany                      | Wymagane approvale | Kto może zatwierdzić |
|---------------------------------|--------------------|----------------------|
| Standardowa funkcja / bugfix    | 1                  | Dowolny senior lub tech lead |
| Zmiany w auth, płatnościach, security | 2           | Co najmniej jeden tech lead |
| Migracje bazy danych            | 1 + review DBA     | Tech lead + wyznaczony reviewer |
| Zmiany w pipeline AI / RAG      | 1                  | Preferowany członek zespołu AI |
| Tylko dokumentacja              | 0 (self-merge OK)  | — |

## Wytyczne dla Pull Requestów

### Przed otwarciem PR
- [ ] Kod buduje się i testy przechodzą lokalnie
- [ ] Wykonałeś(-aś) self-review diffa
- [ ] Opis PR wyjaśnia *dlaczego*, a nie tylko *co*
- [ ] Podlinkowany ticket z Linear (jeśli dotyczy)
- [ ] Screenshoty / nagrania dla zmian UI

### Rozmiar PR
- Preferujemy PR-y poniżej **400 linii** istotnej zmiany kodu.
- Większe zmiany, jeśli to możliwe, dziel na stacked PR.

### Czas odpowiedzi na review
- Reviewer powinien odpowiedzieć w ciągu **1 dnia roboczego**.
- Jeśli jest blokada, zostaw komentarz i przejdź dalej — nie zostawiaj PR-ów w zawieszeniu.

## Na co reviewer powinien zwracać uwagę

1. **Correctness** – czy zmiana robi to, co deklaruje?
2. **Readability** – czy ktoś zrozumie to za 6 miesięcy?
3. **Testy** – czy kluczowe ścieżki są pokryte?
4. **Security** – sekrety, ryzyka wstrzyknięć, zbyt szerokie uprawnienia?
5. **Performance** – oczywiste N+1 lub zbyt duże payloady?
6. **Consistency** – zgodność z istniejącymi wzorcami w repo?

## Approval i merge

- W GitHub używaj „Approve” albo „Request changes”.
- Po approvalu merguje autor (lub reviewer, jeśli autora nie ma).
- Domyślnie używamy squash merge. Rebase tylko gdy historia musi pozostać liniowa.

## Hotfixy

Dla incydentów produkcyjnych:
- Utwórz branch od `main`
- Zdobądź co najmniej jeden approval (w skrajnych przypadkach może być asynchronicznie przez Slack)
- Zmerguj i wdrażaj od razu
- Potem dodaj właściwy ticket post-mortem

## Wyjątki

Tech leadzi mogą czasowo przyznać wyjątki dla pilnych prac klientowskich. Opisz wyjątek w opisie PR.
