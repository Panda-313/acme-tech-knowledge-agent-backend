import logging
from pathlib import Path

from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from ..config import (
    CHROMA_COLLECTION_NAME,
    CHROMA_DB_PATH,
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    DATA_RAW_PATH,
    DOCUMENT_GLOB_PATTERN,
    EMBEDDING_MODEL_NAME,
)

logger = logging.getLogger(__name__)


def load_documents(data_path: Path | str = DATA_RAW_PATH) -> list[Document]:
    data_path = Path(data_path)
    if not data_path.exists():
        logger.error(f"Data path does not exist: {data_path}")
        raise FileNotFoundError(f"Data path does not exist: {data_path}")

    logger.info(f"Loading documents from {data_path}")

    loader = DirectoryLoader(
        path=str(data_path),
        glob=DOCUMENT_GLOB_PATTERN,
        loader_cls=TextLoader,
    )

    documents = loader.load()

    if not documents:
        logger.error("No documents found")
        raise ValueError(f"No markdown documents found in {data_path}")

    logger.info(f"Loaded {len(documents)} documents")
    return documents


def split_documents(
    documents: list[Document],
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP,
) -> list[Document]:
    if not documents:
        logger.error("Documents list is empty")
        raise ValueError("Documents list cannot be empty")

    if chunk_size <= 0:
        logger.error(f"Invalid chunk_size: {chunk_size}")
        raise ValueError("chunk_size must be positive")

    logger.info(
        f"Splitting {len(documents)} documents into chunks "
        f"(size={chunk_size}, overlap={chunk_overlap})"
    )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    chunks = splitter.split_documents(documents)
    logger.info(f"Created {len(chunks)} chunks")
    return chunks


def create_vectorstore(
    chunks: list[Document],
    persist_directory: Path | str = CHROMA_DB_PATH,
    collection_name: str = CHROMA_COLLECTION_NAME,
    model_name: str = EMBEDDING_MODEL_NAME,
) -> Chroma:
    if not chunks:
        logger.error("Chunks list is empty")
        raise ValueError("Chunks list cannot be empty")

    logger.info(f"Creating vectorstore with collection: {collection_name}")
    logger.info(f"Using embedding model: {model_name}")

    embeddings = HuggingFaceEmbeddings(model_name=model_name)

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(persist_directory),
        collection_name=collection_name,
    )

    logger.info(f"Vectorstore created and persisted at {persist_directory}")
    return vectorstore


def ingest_documents(
    data_path: Path | str = DATA_RAW_PATH,
    persist_directory: Path | str = CHROMA_DB_PATH,
    collection_name: str = CHROMA_COLLECTION_NAME,
) -> Chroma:
    logger.info("Starting document ingestion pipeline")

    documents: list[Document] = load_documents(data_path)
    chunks: list[Document] = split_documents(documents)
    vectorstore = create_vectorstore(chunks, persist_directory, collection_name)

    logger.info("Document ingestion pipeline completed successfully")
    return vectorstore
