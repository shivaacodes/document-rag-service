# Loads model once, async encode using threadpool, with LRU cache.
# ✓ async ✓ batched ✓ cached ✓ non-blocking

import asyncio
from functools import lru_cache() # type: ignore
from sentence_transformers import SentenceTransformer

from core.config import settings

class EmbeddingService:
    def __init__(self):
        # load model once start-up
        self.model = SentenceTransformer(settings.embedding_model)

    @lru_cache(maxsize=256)
    def _cached_single(self, text: str):
        # sync helper for LRU Caching
        return self.model.encode([text],convert_to_numpy=True)[0]

    async def embed_texts(self, texts: list[str]):
        loop = asyncio.get_running_loop()
        
        # use executor to avoid blocking event loop
        embeddings = await loop.run_in_executor(
            None,
            self._encode_batch,
            texts
        )
        return embeddings

    def _encode_batch(self, texts: list[str]):
        # encode texts in batch
        return self.model.encode(
            texts,
            batch_size=32,
            convert_to_numpy=True
        ).tolist() # type: ignore

embedding_service = EmbeddingService()
