from typing import Any, Dict, List
from .embeddings import embedding_service
from .vectorstore import vectorstore
import structlog
import time
from opentelemetry import trace

logger = structlog.get_logger("retrieval")
tracer = trace.get_tracer(__name__)


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
    with tracer.start_as_current_span("retrieval_pipeline") as parent_span:
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
        with tracer.start_as_current_span("embed_query") as embed_span:
            query_embedding = await embedding_service.embed_texts([query])

        chroma_collection = vectorstore.collection

        with tracer.start_as_current_span("vectorstore_query") as query_span:
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

        parent_span.set_attribute("chunk_count", chunk_count)
        parent_span.set_attribute("retrieval_ms", retrieval_ms)


        logger.info(
            "retrieval_completed",
            query_len=len(query),
            chunks=chunk_count,
            retrieval_ms=retrieval_ms,
        )

        return output
