# FAQ dla developerów

Szybkie odpowiedzi na pytania, które pojawiają się najczęściej. Jeśli czegoś brakuje, dodaj to przez PR.

## Ogólne

**P: Gdzie jest główny kod projektu?**  
O: `github.com/acmetech/platform` (monorepo). Frontend jest w `/apps/web`, backend w `/services`.

**P: Jak uzyskać dostęp do logów produkcyjnych?**  
O: Zapytaj na `#devops`. Dostęp jest nadawany przez AWS SSO po akceptacji.

**P: Jak nazywamy branche?**  
O: `feat/short-description`, `fix/ticket-123`, `chore/...`. Jeśli to możliwe, dodawaj ID ticketa z Linear.

## Rozwój lokalny

**P: Docker zjada cały RAM. Co mogę zrobić?**  
O: Uruchamiaj `docker compose up` tylko dla usług, których potrzebujesz. Wiele osób uruchamia lokalnie Postgresa i Redisa, a konteneryzuje tylko resztę.

**P: Jak zresetować lokalną bazę danych?**  
O: `make db-reset` (albo `alembic downgrade base && alembic upgrade head` + skrypt seedujący).

**P: Frontend hot reload działa wolno.**  
O: Upewnij się, że masz najnowsze Angular CLI i builder oparty o esbuild. Spróbuj też czasowo wyłączyć source mapy.

## AI / RAG

**P: Czy mogę używać dokumentów firmowych w publicznym ChatGPT?**  
O: Nie. Zobacz `ai-usage-guidelines.md`. Używaj modeli lokalnych albo firmowo zatwierdzonych endpointów.

**P: Jak przetestować lokalnie Knowledge Bota?**  
O: Postępuj zgodnie z README w `/services/knowledge-bot`. Potrzebujesz uruchomionego ChromaDB i zindeksowanych dokumentów Markdown.

**P: Jaki model embeddingów wybrać na start eksperymentów?**  
O: Zacznij od `all-MiniLM-L6-v2` (lokalny, szybki, darmowy). Na embeddingi OpenAI przechodź dopiero, gdy potrzebujesz wyższej jakości i masz akceptację budżetu.

## Proces

**P: Czy do każdego PR potrzebuję ticketa w Linear?**  
O: Dla wszystkiego większego niż literówka lub drobna poprawka — tak. Pomaga to w priorytetyzacji i późniejszym audycie.

**P: Kto decyduje o dodawaniu nowych bibliotek?**  
O: Tech leadzi + krótka dyskusja na `#engineering`. Staramy się nie dodawać zależności pochopnie.

**P: Jak często deployujemy?**  
O: Usługi backendowe: kilka razy dziennie. Frontend: ciągle po merge do `main` (z feature flagami, jeśli potrzeba).

## Nadal utknąłeś(-ęłaś)?

Zapytaj na `#engineering` lub na odpowiednim kanale zespołu. Ktoś pomoże.
