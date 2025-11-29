import pytest
from httpx import AsyncClient
from unittest.mock import patch

@pytest.mark.asyncio
async def test_upload_endpoint_success(client: AsyncClient, sample_pdf_bytes):
    with patch("app.api.routes_upload.ingestion_service.ingest") as mock_ingest:
        mock_ingest.return_value = {"status": "ingested", "chunks": 1, "filename": "test.pdf"}
        
        response = await client.post(
            "/upload", 
            files={"file": ("test.pdf", sample_pdf_bytes, "application/pdf")},
            headers={"X-API-Key": "local-dev-key"}
        )
        
        assert response.status_code == 200
        assert response.json()["status"] == "ingested"
        mock_ingest.assert_called_once()

@pytest.mark.asyncio
async def test_upload_endpoint_invalid_file_type(client: AsyncClient):
    response = await client.post(
        "/upload", 
        files={"file": ("test.exe", b"content", "application/octet-stream")},
        headers={"X-API-Key": "local-dev-key"}
    )
    
    assert response.status_code == 400
