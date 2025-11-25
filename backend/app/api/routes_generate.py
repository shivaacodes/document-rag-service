from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..services.retrieval import retrieve_relevant_chunks
from ..services.llm import generate_answer
import structlog
import time

router = APIRouter()
logger = structlog.get_logger("api_generate")


class GenerateRequest(BaseModel):
    query: str
    top_k: int = 5


@router.post("/generate")
async def generate_endpoint(payload: GenerateRequest):
    if not payload.query.strip():
        logger.warning(
            "generate_missing_query",
            query_len=0,
            top_k=payload.top_k,
        )
        raise HTTPException(status_code=400, detail="Query text is required")

    total_start = time.time()

    # retrieval
    chunks = await retrieve_relevant_chunks(
        query=payload.query,
        top_k=payload.top_k,
    )

    if not chunks:
        logger.info(
            "generate_no_chunks",
            query_len=len(payload.query),
            top_k=payload.top_k,
            chunks=0,
        )
        return {"answer": "I could not find any relevant information in the documents."}

    # llm
    answer = await generate_answer(
        query=payload.query,
        chunks=chunks
    )

    total_ms = (time.time() - total_start) * 1000

    logger.info(
        "generate_completed",
        query_len=len(payload.query),
        chunks=len(chunks),
        top_k=payload.top_k,
        total_ms=total_ms,
        answer_len=len(answer),
    )

    return {
        "answer": answer,
        "chunks": chunks
    }
