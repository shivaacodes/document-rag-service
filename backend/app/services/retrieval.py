from typing import Any, Dict, List
from .embeddings import embedding_service
from .vectorstore import vectorstore
import structlog
import time

logger = structlog.get_logger("retrieval")


async def retrieve_relevant_chunks(
    query: str, 
    top_k: int = 5
) -> List[Dict[str,Any]]:
    """
    Retrieval Pipeline
    1. Embed query.
    2. Query Chroma
    3. Return matched documents with metadata and score.
    """

    start_time = time.time()

    if not query or not query.strip():
        logger.info(
            "retrieval empty query",
            query_len=0,
            chunks=0,
            retrieval_ms=0.0,
        )
        return []

    # embed query as 1-item list
    query_embedding = await embedding_service.embed_texts([query])

    chroma_collection = vectorstore.collection

    results = chroma_collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )


    # standardize return format
    documents_list = results.get("documents")
    documents = documents_list[0] if documents_list else []

    metadatas_list = results.get("metadatas")
    metadatas = metadatas_list[0] if metadatas_list else []

    distances_list = results.get("distances")
    distances = distances_list[0] if distances_list else []

    output = []
    for doc, meta, dist in zip(documents,metadatas,distances):
        output.append(
            {
                "text": doc,
                "metadata": meta,
                "score": float(dist),
            }
        )

    retrieval_ms = (time.time() - start_time) * 1000
    chunk_count = len(output)

    logger.info(
        "retrieval_completed",
        query_len=len(query),
        chunks=chunk_count,
        retrieval_ms=retrieval_ms,
    )

    return output
