# /query → retrieve top chunks from Chroma

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..services.retrieval import retrieve_relevant_chunks


router = APIRouter()

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5

@router.post("")
async def query_endpoint(payload: QueryRequest):
    if not payload.query.strip():
        raise HTTPException(status_code=400, detail="Query text is required")

    results = await retrieve_relevant_chunks(
        query=payload.query,
        top_k=payload.top_k,
    )

    return {"results" : results}
