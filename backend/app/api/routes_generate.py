from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..services.retrieval import retrieve_relevant_chunks
from ..services.llm import generate_answer

router = APIRouter()

class GenerateRequest(BaseModel):
    query: str
    top_k: int = 5

@router.post("/generate")
async def generate_endpoint(payload: GenerateRequest):
    if not payload.query.strip():
        raise HTTPException(status_code=400, detail="Query text is required")

    # 1. Retrieve relevant chunks
    chunks = await retrieve_relevant_chunks(
        query=payload.query,
        top_k=payload.top_k,
    )

    if not chunks:
        return {"answer": "I could not find any relevant information in the documents."}

    # 2. Generate answer from chunks
    answer = await generate_answer(query=payload.query, chunks=chunks)

    return {"answer": answer, "chunks": chunks}
