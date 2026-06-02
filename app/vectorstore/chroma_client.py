import os
import chromadb
from app.core.logging import get_logger

logger = get_logger(__name__)


def get_chroma_client() -> chromadb.ClientAPI:
    """Initialize and return a ChromaDB client.

    Supports HTTP client (for Docker Compose/production) or local persistent
    database.
    """
    chroma_host = os.getenv("CHROMA_HOST")
    chroma_port = os.getenv("CHROMA_PORT", "8000")

    if chroma_host:
        logger.info("Initializing Chroma HTTP client", host=chroma_host, port=chroma_port)
        return chromadb.HttpClient(host=chroma_host, port=int(chroma_port))
    else:
        # Fallback to local persistent database
        db_path = os.getenv("CHROMA_PERSIST_PATH", "./storage/chroma_db")
        os.makedirs(db_path, exist_ok=True)
        logger.info("Initializing Chroma persistent client", path=db_path)
        return chromadb.PersistentClient(path=db_path)
