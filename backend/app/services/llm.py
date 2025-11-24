# generation layer
# Q&A over documents

import httpx
from typing import List, Dict, Any

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral"

async def generate_answer(query: str, chunks: List[Dict[str, Any]]) -> str:
    context = "\n\n".join([c["text"] for c in chunks])

    prompt = (
        "You are a RAG assistant. Use only the context provided."
        "\n\nContext:\n"
        f"{context}"
        "\n\nQuestion:\n"
        f"{query}"
        "\n\nAnswer using only the context. If not found, respond that the information is not available."
    )

    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            }
        )

    if response.status_code != 200:
        return f"LLM error: {response.text}"

    data = response.json()
    return data.get("response", "").strip()

