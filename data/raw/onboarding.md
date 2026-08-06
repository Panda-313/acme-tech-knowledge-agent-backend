# Przewodnik onboardingowy AcmeTech

Witamy w AcmeTech! Budujemy kolejną generację aplikacji Angular + AI. Ten przewodnik pomoże Ci szybko wejść w pracę podczas pierwszych dwóch tygodni.

## Pierwszy dzień

1. **Konta i dostępy**
   - Slack (workspace firmy) – dołącz do `#general`, `#engineering`, `#ai-experiments`
   - GitHub Enterprise – poproś o dostęp przez ticket IT
   - 1Password – firmowy vault zostanie Ci udostępniony
   - Google Workspace – kalendarz, Drive, email
   - Linear – zarządzanie projektami (zaproszenie wyśle manager)

2. **Sprzęt**
   - MacBook Pro M-series (lub stacja Linux, jeśli wolisz)
   - Monitor zewnętrzny i stacja dokująca dostępne na życzenie

3. **Materiały obowiązkowe (dzień 1)**
   - `tech-stack.md`
   - `security-basics.md`
   - `ai-usage-guidelines.md`
   - Wartości firmy (udostępnione na Drive)

## Checklista na 1. tydzień

- [ ] Skonfiguruj lokalne środowisko deweloperskie (zob. `tech-stack.md`)
- [ ] Ukończ szkolenie security (30 min, link na Slacku)
- [ ] Zrób pairing z buddy na małym tickecie
- [ ] Weź udział w cotygodniowym Engineering Sync (wtorek 10:00)
- [ ] Przedstaw się na `#engineering` krótką notką o swoim doświadczeniu

## Konfiguracja środowiska developerskiego

```bash
# Sklonuj główne monorepo
git clone git@github.com:acmetech/platform.git
cd platform

# Zainstaluj zależności
npm install          # frontend
pip install -r requirements.txt  # backend

# Uruchom lokalne usługi
docker compose up -d   # Postgres, Redis, Chroma
```

Pełna instrukcja setupu znajduje się w `README.md` repo platformy.

## Kultura i komunikacja

- Cenimy **ownership** i **bezpośredni feedback**.
- Domyślnie preferujemy komunikację asynchroniczną (komentarze w Linear, wątki na Slacku).
- Spotkania mają agendy i notatki. Jeśli spotkanie nie ma agendy, możesz je odrzucić.
- Dostarczamy małe zmiany, ale często. Tam, gdzie to możliwe, preferujemy PR-y poniżej 400 linii.

## Kluczowe osoby

| Rola                  | Imię i nazwisko | Slack |
|-----------------------|------------------|-------|
| Engineering Manager   | Anna Kowalska    | @anna |
| Tech Lead (Frontend)  | Marek Nowak      | @marek |
| Tech Lead (AI)        | Sofia Rivera     | @sofia |
| People Ops            | Tom Ellis        | @tom |

## Pytania?

Zapytaj na `#onboarding` albo napisz do managera. W pierwszym miesiącu nie ma głupich pytań.

Witamy na pokładzie — cieszymy się, że jesteś z nami.
