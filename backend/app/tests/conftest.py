import sys
from unittest.mock import MagicMock, AsyncMock, patch

# Mock chromadb before importing app to avoid connection errors during collection
sys.modules["chromadb"] = MagicMock()
sys.modules["chromadb"].HttpClient = MagicMock()

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app
from typing import AsyncGenerator
from app.services.vectorstore import vectorstore as real_vectorstore
from app.services.embeddings import embedding_service as real_embedding_service

@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """
    Fixture for async HTTP client against the FastAPI app.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

@pytest.fixture
def mock_vectorstore():
    """
    Mock the VectorStore dependency using patch.object on the singleton.
    """
    # We patch the methods/attributes on the real singleton instance
    with patch.object(real_vectorstore, 'collection') as mock_collection, \
         patch.object(real_vectorstore, 'clear') as mock_clear, \
         patch.object(real_vectorstore, 'add_documents') as mock_add:
        
        mock_collection.count.return_value = 0
        mock_collection.query.return_value = {
            "documents": [[]],
            "metadatas": [[]],
            "distances": [[]]
        }
        
        # Attach the mocks to the singleton so we can assert on them
        real_vectorstore.collection = mock_collection
        real_vectorstore.clear = mock_clear
        real_vectorstore.add_documents = mock_add
        
        yield real_vectorstore

@pytest.fixture
def mock_embedding_service():
    """
    Mock the EmbeddingService dependency using patch.object on the singleton.
    """
    with patch.object(real_embedding_service, 'embed_texts', new_callable=AsyncMock) as mock_embed:
        mock_embed.side_effect = lambda texts: [[0.1] * 384 for _ in texts]
        yield real_embedding_service

@pytest.fixture
def mock_llm_service():
    """
    Mock the LLM generation service.
    """
    with patch("app.api.routes_generate.generate_answer", new_callable=AsyncMock) as mock:
        mock.return_value = "This is a mocked answer from the LLM."
        yield mock

@pytest.fixture
def sample_pdf_bytes():
    """
    Return dummy PDF bytes for testing uploads.
    """
    return b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Kids [3 0 R]\n/Count 1\n/Type /Pages\n>>\nendobj\n3 0 obj\n<<\n/MediaBox [0 0 595 842]\n/Type /Page\n/Parent 2 0 R\n/Resources <<\n/Font <<\n/F1 4 0 R\n>>\n>>\n/Contents 5 0 R\n>>\nendobj\n4 0 obj\n<<\n/Type /Font\n/Subtype /Type1\n/BaseFont /Helvetica\n>>\nendobj\n5 0 obj\n<<\n/Length 44\n>>\nstream\nBT\n/F1 24 Tf\n100 100 Td\n(Hello World) Tj\nET\nendstream\nendobj\nxref\n0 6\n0000000000 65535 f\n0000000010 00000 n\n0000000060 00000 n\n0000000117 00000 n\n0000000258 00000 n\n0000000345 00000 n\ntrailer\n<<\n/Size 6\n/Root 1 0 R\n>>\nstartxref\n439\n%%EOF"
