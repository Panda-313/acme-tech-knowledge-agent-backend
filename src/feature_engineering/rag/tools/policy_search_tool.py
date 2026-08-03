import logging

from langchain_core.tools import tool

from src.feature_engineering.config import POLICY_MAP, DATA_RAW_PATH


def build_policy_search_tool(
        logger: logging.Logger,
        used_sources: list[str],
):
    @tool("policy_search_tool", description="""Pobiera pełną treść konkretnej polityki lub wytycznych AcmeTech po nazwie.

Użyj tego narzędzia gdy użytkownik:
- Prosi o konkretną politykę po nazwie (np. "Pokaż mi politykę urlopową")
- Chce pełny dokument, nie tylko fragmenty
- Używa fraz typu "Jakie są zasady...", "Pokaż mi wytyczne dotyczące...", "Daj mi politykę X"

Dostępne polityki: vacation, remote_work, ai_usage, code_review, security, deployment, incident_response, testing, api_design, performance, knowledge_sharing, onboarding, architecture, tech_stack, team_structure, roadmap, faq

NIE używaj tego narzędzia gdy:
- Pytanie jest ogólne lub eksploracyjne → użyj search_docs
- Użytkownik chce streszczenie → użyj summarize_document
- Nazwa polityki nie pasuje do żadnej dostępnej opcji

Input: nazwa polityki (np. "vacation", "ai_usage", "code_review")""")
    def policy_search(policy_name : str) -> str:
        policy_name = policy_name.lower().strip()

        if policy_name not in POLICY_MAP:
            available_policies = ", ".join(POLICY_MAP.keys())

            return f"Unknown policy: {policy_name}. Available policies: {available_policies}"

        file_name = POLICY_MAP[policy_name]
        file_path = DATA_RAW_PATH / file_name

        logger.info(f"Retriving policy document: {policy_name} from {file_path}")

        if not file_path.exists():
            return f"Couldnt find the policy with path: {file_path}"

        content = file_path.read_text(encoding="utf-8")

        if file_path not in used_sources:
            used_sources.append(file_name)

        return content

    return policy_search


