from fastapi import APIRouter, HTTPException
import httpx
from ..services.vectorstore import vectorstore
from ..services.llm import OLLAMA_URL

router = APIRouter()

@router.get("/health", status_code=200)
async def health_check():
    try:
        # Check ChromaDB connection
        vectorstore.client.heartbeat()
        chroma_status = "ok"
    except Exception as e:
        chroma_status = f"error: {e}"

    try:
        # Check Ollama connection
        ollama_base_url = OLLAMA_URL.replace("/api/generate", "")
        async with httpx.AsyncClient() as client:
            response = await client.get(ollama_base_url)
            response.raise_for_status()
        ollama_status = "ok"
    except Exception as e:
        ollama_status = f"error: {e}"

    status = {
        "chromadb": chroma_status,
        "ollama": ollama_status,
    }

    if chroma_status != "ok" or ollama_status != "ok":
        raise HTTPException(status_code=503, detail=status)

    return status
