import pytest
from httpx import AsyncClient
from unittest.mock import patch

@pytest.mark.asyncio
async def test_e2e_workflow(client: AsyncClient, sample_pdf_bytes):
    # Mock all external services to test the flow through the API layer
    with patch("app.api.routes_upload.ingestion_service.ingest") as mock_ingest, \
         patch("app.api.routes_generate.retrieve_relevant_chunks") as mock_retrieve, \
         patch("app.api.routes_generate.generate_answer") as mock_generate:
        
        # Setup mocks
        mock_ingest.return_value = {"status": "ingested", "chunks": 1, "filename": "test.pdf"}
        mock_retrieve.return_value = [{"text": "Chunk 1", "score": 0.1, "metadata": {}}]
        mock_generate.return_value = "Generated Answer"
        
        # 1. Upload
        upload_res = await client.post(
            "/upload", 
            files={"file": ("test.pdf", sample_pdf_bytes, "application/pdf")},
            headers={"X-API-Key": "local-dev-key"}
        )
        assert upload_res.status_code == 200
        
        # 2. Generate (RAG)
        generate_res = await client.post(
            "/api/generate", 
            json={"query": "test query"},
            headers={"X-API-Key": "local-dev-key"}
        )
        assert generate_res.status_code == 200
        assert generate_res.json()["answer"] == "Generated Answer"
        
        # Verify calls
        mock_ingest.assert_called_once()
        mock_retrieve.assert_called_once()
        mock_generate.assert_called_once()
