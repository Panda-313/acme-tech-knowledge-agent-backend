# Wytyczne korzystania z AI w AcmeTech

Ostatnia aktualizacja: czerwiec 2026

## Cel

Te wytyczne pomagają produktywnie korzystać z narzędzi AI przy jednoczesnej ochronie danych firmy, prywatności klientów i jakości kodu.

## Dozwolone narzędzia

| Narzędzie              | Dozwolone | Uwagi |
|------------------------|-----------|-------|
| GitHub Copilot         | ✅        | Licencja firmowa |
| Cursor / Windsurf      | ✅        | Z kontem firmowym |
| ChatGPT / Claude (web) | ✅        | **Nie** wklejaj sekretów ani danych klientów |
| Groq / OpenAI API      | ✅        | Używaj tylko firmowych kluczy |
| Modele lokalne (Ollama)| ✅        | Preferowane dla wrażliwego kodu |
| Publiczne darmowe narzędzia | ⚠️   | Tylko dla treści niewrażliwych i niezastrzeżonych |

## Złote zasady

1. **Nigdy nie wklejaj sekretów, kluczy API, haseł ani PII klientów** do zewnętrznych narzędzi AI.
2. **Nigdy nie commituj kodu wygenerowanego przez AI bez review.** Odpowiadasz za każdą linię, która trafia do `main`.
3. Przy pracy z dokumentami wewnętrznymi lub danymi klientów preferuj **modele lokalne** (Ollama) albo firmowo zatwierdzone API.
4. AI to **pair programmer**, nie autor. Musisz rozumieć kod, który wysyłasz.
5. Korzystając z AI przy decyzjach architektonicznych lub projektowych, dokumentuj uzasadnienie w PR albo tickecie Linear.

## Co jest zalecane

- Generowanie boilerplate’u, testów i szkiców dokumentacji
- Wyjaśnianie nieznanego kodu lub komunikatów błędów
- Burza mózgów nad alternatywnymi implementacjami
- Pisanie commit message i opisów PR
- Tworzenie syntetycznych danych testowych
- Budowa wewnętrznych prototypów RAG (jak ten Knowledge Bot)

## Co jest odradzane / zabronione

- Wysyłanie dużych PR-ów wygenerowanych przez AI bez sensownego review człowieka
- Używanie publicznych narzędzi AI z produkcyjnymi schematami bazy lub realnymi danymi klientów
- Generowanie kodu omijającego nasze wzorce bezpieczeństwa i uwierzytelniania
- Poleganie na AI przy finalnych decyzjach architektonicznych bez dyskusji z zespołem

## RAG i wiedza wewnętrzna

Aktywnie budujemy wewnętrzne systemy RAG (zob. inicjatywa Knowledge Bot).  
Wnosząc wkład do tych systemów:

- Indeksuj wyłącznie dokumenty zatwierdzone do dystrybucji wewnętrznej
- Nie indeksuj danych klientów ani danych osobowych pracowników bez wyraźnej zgody Legal/People Ops
- Zawsze pokazuj źródła w odpowiedziach, jeśli system to wspiera

## Zgłaszanie incydentów

Jeśli wykryjesz, że dane wrażliwe zostały przypadkowo wysłane do zewnętrznego modelu, natychmiast powiadom `#security`.

Pytania o te wytyczne → napisz na `#ai-experiments` lub do Sofii (@sofia).
