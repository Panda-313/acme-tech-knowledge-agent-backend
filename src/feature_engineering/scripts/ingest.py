import logging
import sys

from src.feature_engineering import ingest_documents
from src.feature_engineering.config import LOG_FORMAT, LOG_LEVEL, DATA_RAW_PATH, CHROMA_DB_PATH

logger = logging.getLogger(__name__)


def setup_logging() -> None:
    logging.basicConfig(
        format=LOG_FORMAT,
        level=LOG_LEVEL,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("ingestion.log"),
        ],
    )


def main() -> int:
    setup_logging()
    logger.info("Starting document ingestion")

    try:
        vectorstore = ingest_documents(
            data_path=DATA_RAW_PATH,
            persist_directory=CHROMA_DB_PATH,
        )
        logger.info("✓ Ingestion completed successfully")
        print("\n✓ Documents ingested successfully!")
        print(f"  Vector store saved to: {CHROMA_DB_PATH}")
        return 0

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        print(f"\n✗ Error: {e}", file=sys.stderr)
        return 1

    except ValueError as e:
        logger.error(f"Validation error: {e}")
        print(f"\n✗ Error: {e}", file=sys.stderr)
        return 1

    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        print(f"\n✗ Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
