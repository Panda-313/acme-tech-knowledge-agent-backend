# Roadmap produktowy AcmeTech 2026

Status: dokument żywy — ostatnia duża aktualizacja: lipiec 2026

## Wizja

Stać się platformą pierwszego wyboru dla firm, które chcą dostarczać aplikacje Angular wzbogacone o niezawodne i ugruntowane funkcje AI.

## Q3 2026 (lipiec – wrzesień)

### Platforma
- [ ] Knowledge Bot v1 (wewnętrzny chatbot RAG) – **w toku**
- [ ] Ujednolicone uwierzytelnianie we wszystkich narzędziach wewnętrznych (OIDC)
- [ ] Ulepszony portal deweloperski z API playground

### Możliwości AI
- [ ] Produkcyjny framework ewaluacji RAG
- [ ] Wsparcie dla wyszukiwania hybrydowego (wektor + słowo kluczowe)
- [ ] Podstawowe workflow agentowe dla wewnętrznych ticketów wsparcia

### Frontend
- [ ] Design system v2 (Angular Material + własne tokeny)
- [ ] Tryb ciemny we wszystkich produktach
- [ ] Egzekwowanie budżetów wydajnościowych w CI

## Q4 2026 (październik – grudzień)

### Platforma
- [ ] Wsparcie multi-tenant dla klientów zewnętrznych
- [ ] Prototyp rozliczeń usage-based
- [ ] Audit logi dla wszystkich interakcji AI

### Możliwości AI
- [ ] Upload dokumentów + automatyczny pipeline indeksacji
- [ ] Poprawa jakości cytowań + podświetlanie źródeł
- [ ] Lokalny fallback modelu (Ollama) dla środowisk offline / wrażliwych

### Developer Experience
- [ ] Lokalny setup „one-click” z pre-seedowanymi danymi
- [ ] Lepsze komunikaty błędów i sugestie samonaprawy w CLI

## Wczesne tematy na 2027 (jeszcze niezatwierdzone)

- Interfejs głosowy dla Knowledge Bota
- Orkiestracja multi-agentowa dla złożonych wewnętrznych procesów
- Publiczny marketplace reużywalnych komponentów AI zbudowanych na naszej platformie

## Zasady priorytetyzacji

1. **Najpierw niezawodność** – nie wdrażamy funkcji AI, które halucynują krytyczne informacje
2. **Developer experience** – jeśli nasze własne zespoły cierpią, klienci też będą cierpieć
3. **Mierzalny wpływ** – każda duża inicjatywa ma zdefiniowane metryki sukcesu

## Jak wpływać na roadmapę

- Otwórz ticket w Linear z etykietą `roadmap-idea`
- Omów temat na comiesięcznym syncu Product & Engineering
- Porozmawiaj bezpośrednio z tech leadem lub odpowiednikiem po stronie produktu

Właścicielem tego dokumentu jest leadership Product + Engineering. Aktualizacja następuje co najmniej raz na kwartał.
