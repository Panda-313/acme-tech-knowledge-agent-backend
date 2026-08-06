# Wytyczne testowania

## Filozofia

Piszemy testy, które dają pewność przy refaktorze i szybkim dowożeniu zmian.  
**Nie** celujemy w 100% pokrycia — celujemy w wysoką pewność na ścieżkach, które naprawdę mają znaczenie.

## Piramida testów (wersja praktyczna)

| Typ               | Narzędzia                         | Kiedy pisać                              | Oczekiwana szybkość |
|-------------------|-----------------------------------|------------------------------------------|---------------------|
| Unit              | Jest (FE) / pytest (BE)           | Czysta logika, utility, serwisy          | Bardzo szybko       |
| Component         | Angular Testing Library           | Komponenty UI z nietrywialną logiką      | Szybko              |
| Integration       | pytest + httpx / TestClient       | Endpointy API, interakcje z bazą         | Średnio             |
| End-to-End        | Playwright                        | Krytyczne ścieżki użytkownika            | Wolniej             |
| AI / RAG eval     | Custom scripts + Ragas            | Jakość odpowiedzi, trafność retrievalu   | Może być wolno      |

## Frontend

- Gdzie to możliwe, preferuj zapytania Testing Library (`getByRole`, `getByLabelText`) zamiast test ID.
- Testuj zachowanie widoczne dla użytkownika, nie szczegóły implementacyjne.
- Snapshot testy stosuj oszczędnie (głównie przy złożonych komponentach prezentacyjnych).

## Backend

- Używaj fixture’ów i factory w `pytest` (factory-boy lub polyfactory).
- Preferuj testy na realnej testowej bazie (Docker), zamiast ciężkiego mockowania ORM.
- Oznaczaj wolne testy `@pytest.mark.slow`, by można je było pominąć w szybkim lokalnym przebiegu.

## Specyfika AI / RAG

Dla Knowledge Bota i podobnych systemów utrzymujemy mały „golden set” pytań:

- Oczekiwana odpowiedź powinna zawierać konkretne kluczowe fakty
- Źródła powinny zawierać wskazane dokumenty
- Śledzimy w czasie współczynnik halucynacji i precyzję retrievalu

Przed mergem istotnych zmian w retrievalu lub promptingu uruchom zestaw ewaluacyjny.

## Co musi być przetestowane przed mergem

- Nowe endpointy API → co najmniej happy path + jeden case błędny
- Logika biznesowa obsługująca pieniądze, uprawnienia lub usuwanie danych
- Zmiany w pipeline RAG → zbiór ewaluacyjny nadal powinien przechodzić
- Flow UI będące częścią krytycznej ścieżki (logowanie, główny chat itd.)

## Continuous Integration

- Wszystkie testy uruchamiają się na każdym PR
- Testy E2E uruchamiają się na `main` oraz na PR, które dotykają krytycznych ścieżek
- Raporty coverage są generowane, ale nie stanowią twardego gate’a

## Wskazówki

- Jeśli test jest flaky, napraw go albo usuń. Flaky testy niszczą zaufanie.
- Preferuj mniej testów, ale lepszych, zamiast wielu kruchych.
- Gdy masz wątpliwości, zapytaj: „Jeśli to się zepsuje, czy test złapie to zanim zobaczy to użytkownik?”
