# Struktura zespołów

Stan na lipiec 2026

## Organizacja Engineering

```
CTO
└── VP Engineering
    ├── Platform Team
    ├── Product Frontend Team
    ├── AI / Knowledge Team
    └── Developer Experience & Infrastructure
```

## Zespoły i odpowiedzialności

### Platform Team
- Kluczowe usługi backendowe
- Uwierzytelnianie i autoryzacja
- Biblioteki współdzielone i wewnętrzne API
- Baza danych i modelowanie danych

### Product Frontend Team
- Aplikacje Angular skierowane do klientów
- Design system
- Dostępność i wydajność UI

### AI / Knowledge Team
- Systemy RAG i Knowledge Bot
- Integracje LLM i ewaluacja
- Wewnętrzne narzędzia AI i eksperymenty
- Prompt engineering i bezpieczeństwo

### Developer Experience & Infrastructure
- Pipeline’y CI/CD
- Doświadczenie lokalnego developmentu
- Observability i monitoring
- Infrastruktura chmurowa

## Role

| Rola                    | Typowy zakres                               |
|-------------------------|---------------------------------------------|
| Software Engineer       | Dostarczanie funkcji w obrębie zespołu      |
| Senior Software Engineer| Techniczne prowadzenie większych inicjatyw  |
| Tech Lead               | Architektura + mentoring + odpowiedzialność za delivery |
| Engineering Manager     | Ludzie, proces, rekrutacja, rozwój kariery  |
| Staff / Principal       | Kierunek techniczny między zespołami        |

## Grupy przekrojowe

- **Security Champions** – jedna osoba na zespół
- **AI Guild** – otwarte dla osób zainteresowanych AI (spotkania co dwa tygodnie)
- **Frontend Guild** – dobre praktyki Angular i rozwój design systemu

## Podejmowanie decyzji

- Decyzje techniczne na poziomie zespołu: Tech Lead + konsensus zespołu
- Decyzje międzyzespołowe lub architektoniczne: RFC + Architecture Review (preferowane asynchronicznie)
- Decyzje kadrowe: Engineering Managerowie + leadership

## On-call

- Obecnie formalne rotacje on-call mają tylko usługi Platform i AI
- Zespoły Frontend i DX wspierają obsługę incydentów, gdy jest taka potrzeba
- Zasady wynagradzania i rotacji on-call są opisane w People Ops

## Jak znaleźć właściwą osobę

- Sprawdź roster zespołów w Linear lub Notion
- Zapytaj na `#engineering` — ktoś wskaże właściwy kierunek
- W tematach people-related → Twój Engineering Manager albo People Ops
