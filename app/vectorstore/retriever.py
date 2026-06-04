from typing import Any, Dict, List
from app.vectorstore.chroma_client import get_chroma_client
from app.vectorstore.embeddings import get_embeddings
from app.core.logging import get_logger

logger = get_logger(__name__)


async def retrieve_context(
    project_id: int,
    query: str,
    limit: int = 5,
) -> List[Dict[str, Any]]:
    try:
        client = get_chroma_client()
        collection_name = f"project_{project_id}"

        collection = client.get_collection(name=collection_name)

        query_vectors = await get_embeddings(query)
        query_vector = query_vectors[0]

        results = collection.query(
            query_embeddings=[query_vector],
            n_results=limit,
        )

        retrieved_chunks = []
        if results and "documents" in results and results["documents"]:
            docs = results["documents"][0]
            metadatas = results["metadatas"][0] if results["metadatas"] else [{}] * len(docs)
            ids = results["ids"][0]

            for doc, meta, doc_id in zip(docs, metadatas, ids):
                retrieved_chunks.append({
                    "id": doc_id,
                    "content": doc,
                    "metadata": meta,
                })

        return retrieved_chunks
    except Exception as e:
        logger.error("Error retrieving context from ChromaDB", project_id=project_id, error=str(e))
        return []
