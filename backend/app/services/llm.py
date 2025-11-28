# generation layer
# Q and A over documents

import httpx
import time
from typing import List, Dict, Any
import structlog
from opentelemetry import trace

OLLAMA_URL = "http://host.docker.internal:11434/api/generate"
MODEL_NAME = "mistral"

logger = structlog.get_logger("llm")
tracer = trace.get_tracer(__name__)


async def generate_answer(query: str, chunks: List[Dict[str, Any]]) -> str:
    start_time = time.time()

    context = "\n\n".join([c["text"] for c in chunks])
    prompt = (
        "You are a RAG assistant. Use only the context provided."
        "\n\nContext:\n"
        f"{context}"
        "\n\nQuestion:\n"
        f"{query}"
        "\n\nAnswer using only the context. If not found, respond that the information is not available."
    )

    with tracer.start_as_current_span("generate_answer") as gen_span:

        try:
            async with httpx.AsyncClient(timeout=60) as client:
                with tracer.start_as_current_span("llm_http_request"):
                    response = await client.post(
                        OLLAMA_URL,
                        json={
                            "model": MODEL_NAME,
                            "prompt": prompt,
                            "stream": False
                        }
                    )
        except Exception as e:
            logger.error(
                "llm_http_error",
                error=str(e),
                query_len=len(query),
                chunks=len(chunks),
                model=MODEL_NAME,
            )
            # Fallback: Return context directly
            return f"**LLM Unavailable (Fallback Mode)**\n\nI couldn't connect to the LLM to generate an answer, but here is the relevant context I found:\n\n{context}"

        if response.status_code != 200:
            logger.error(
                "llm_response_error",
                status=response.status_code,
                body=response.text,
                model=MODEL_NAME,
            )
            return f"**LLM Error (Fallback Mode)**\n\nI encountered an error generating the answer, but here is the relevant context:\n\n{context}"

        data = response.json()
        answer = data.get("response", "").strip()

    llm_ms = (time.time() - start_time) * 1000
    logger.info(
        "llm_completed",
        query_len=len(query),
        chunks=len(chunks),
        llm_ms=llm_ms,
        model=MODEL_NAME,
        answer_len=len(answer),
    )

    return answer
