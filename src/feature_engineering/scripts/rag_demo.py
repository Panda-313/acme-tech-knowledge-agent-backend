import logging
import sys

from ..config import CHROMA_COLLECTION_NAME, CHROMA_DB_PATH, LOG_FORMAT, LOG_LEVEL
from ..rag import ask_question, load_vectorstore

logger = logging.getLogger(__name__)

DEMO_QUESTIONS = [
    "Where do we store the codebase?",
    "What should i do if docker is taking to much ram?",
    "How does the onboarding look like?",
    "Czy Ewelina Oleszak to matol?",
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
        for question in DEMO_QUESTIONS:
            print(f"\nPytanie: {question}")
            print("-" * 60)

            response = ask_question(question, vectorstore)
            answer_preview = response[:200]
            print(f"Odpowiedź: {answer_preview}")

            if len(response) > 200:
                print("  [...]")

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
