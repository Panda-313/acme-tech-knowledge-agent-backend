import logging
import sys

from langgraph.checkpoint.memory import InMemorySaver

from src.feature_engineering import ask_question_agent
from ..config import CHROMA_COLLECTION_NAME, CHROMA_DB_PATH, LOG_FORMAT, LOG_LEVEL
from ..models import MockedUser, Year
from ..rag import ask_question, load_vectorstore

logger = logging.getLogger(__name__)

MOCKED_USERS: list[MockedUser] = [
    MockedUser(
        id=1,
        name="Miki",
        free_days_off_left={
            2027: 35,
            2026: 10,
            2025: 2,
            2024: 0,
        },
    ),
    MockedUser(
        id=2,
        name="Ewel",
        free_days_off_left={
            2027: 35,
            2026: 0,
            2025: 0,
            2024: 0,
        },
    ),
]

DEMO_QUESTIONS = [
    "Nazywam sie Miki, szukam informacji na temat firmy acme tech",
    "Przypomnij mi prosze jak sie nazywam. Oraz informacje na temat urlopow",
    # "Ile dni urlopowych zostalo mi w 2026 roku?",
    # "Ile dni urlopowych zostalo mi w 2023 roku?",
    # "Ile urlopu jeszcze mam w tym roku?"
    "Jak wyglada polityka urlopow? Ale daj mi skrocona wersje",
    # "What is the remote work policy?",
]


def setup_logging() -> None:
    logging.basicConfig(
        format=LOG_FORMAT,
        level=LOG_LEVEL,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("rag_demo.log"),
        ],
    )


def main() -> int:
    setup_logging()
    logger.info("Starting RAG demo")

    try:
        vectorstore = load_vectorstore(
            persist_directory=str(CHROMA_DB_PATH),
            collection_name=CHROMA_COLLECTION_NAME,
        )
        logger.info("Vectorstore loaded successfully")

    except Exception as e:
        logger.error(f"Failed to load vectorstore: {e}")
        print(f"\n✗ Error loading vectorstore: {e}", file=sys.stderr)
        print("  Make sure you have run the ingestion script first.", file=sys.stderr)
        return 1

    print("\n" + "=" * 60)
    print("RAG DEMO - AcmeTech Assistant")
    print("=" * 60)

    try:
        checkpointer = InMemorySaver()
        for idx, question  in enumerate(DEMO_QUESTIONS, start = 1):
            print(f"\nPytanie: {question}")
            print("-" * 60)

            response = ask_question_agent(
                question,
                vectorstore,
                MOCKED_USERS[0],
                checkpointer,
                tags=["rag_demo"],
                metadata={"question_id": idx, "thread_id": idx},
            )
            answer_preview = response.answer
            print(f"Odpowiedź: {answer_preview}")

            if response.sources:
                print(f"Źródła: {', '.join(response.sources)}")

            # if len(response.answer) > 400:
            #     print("  [...]")

        logger.info("✓ RAG demo completed successfully")
        print("\n" + "=" * 60)
        print("✓ Demo completed!")
        print("=" * 60 + "\n")
        return 0

    except Exception as e:
        logger.exception(f"Error during RAG demo: {e}")
        print(f"\n✗ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
