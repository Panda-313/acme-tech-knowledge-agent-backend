# Testing Guidelines

## Philosophy

We write tests that give us confidence to refactor and ship quickly.  
We do **not** aim for 100% coverage – we aim for high confidence on the paths that matter.

## Test Pyramid (practical version)

| Type              | Tooling                          | When to write                          | Speed expectation |
|-------------------|----------------------------------|----------------------------------------|-------------------|
| Unit              | Jest (FE) / pytest (BE)          | Pure logic, utilities, services        | Very fast         |
| Component         | Angular Testing Library          | UI components with non-trivial logic   | Fast              |
| Integration       | pytest + httpx / TestClient      | API endpoints, DB interactions         | Medium            |
| End-to-End        | Playwright                       | Critical user journeys                 | Slower            |
| AI / RAG eval     | Custom scripts + Ragas           | Answer quality, retrieval relevance    | Can be slow       |

## Frontend

- Prefer Testing Library queries (`getByRole`, `getByLabelText`) over test IDs when possible.
- Test user-visible behavior, not implementation details.
- Snapshot tests are allowed sparingly (mostly for complex presentational components).

## Backend

- Use `pytest` fixtures and factories (factory-boy or polyfactory).
- Prefer testing against a real test database (Docker) rather than heavy mocking of the ORM.
- Mark slow tests with `@pytest.mark.slow` so they can be skipped in quick local runs.

## AI / RAG Specific

For the Knowledge Bot and similar systems we maintain a small golden set of questions:

- Expected answer should contain certain key facts
- Sources should include specific documents
- We track hallucination rate and retrieval precision over time

Run the evaluation suite before merging significant changes to the retrieval or prompting logic.

## What Must Be Tested Before Merge

- New API endpoints → at least happy path + one error case
- Business logic that handles money, permissions, or data deletion
- Changes to the RAG pipeline → evaluation set should still pass
- UI flows that are part of the critical path (login, main chat, etc.)

## Continuous Integration

- All tests run on every PR
- E2E tests run on `main` and on PRs that touch critical paths
- Coverage reports are generated but not used as hard gates

## Tips

- If a test is flaky, fix it or delete it. Flaky tests destroy trust.
- Prefer fewer, better tests over many brittle ones.
- When in doubt, ask: “If this breaks, will a test catch it before a user does?”
