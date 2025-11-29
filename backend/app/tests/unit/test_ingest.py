import pytest
from unittest.mock import patch, MagicMock
from app.services.ingestion import ingestion_service

@pytest.mark.asyncio
async def test_ingest_pdf_success(sample_pdf_bytes, mock_vectorstore, mock_embedding_service):
    with patch("app.services.ingestion.extract_text_from_pdf") as mock_extract, \
         patch("app.services.ingestion.chunk_text") as mock_chunk:
        
        mock_extract.return_value = "Mocked PDF content"
        mock_chunk.return_value = [{"text": "Mocked PDF content", "chunk_index": 0, "start_token": 0, "end_token": 10}]
        
        result = await ingestion_service.ingest(sample_pdf_bytes, "test.pdf")
        
        assert result["status"] == "ingested"
        assert result["chunks"] == 1
        
        mock_extract.assert_called_once()
        mock_vectorstore.clear.assert_called_once()
        mock_embedding_service.embed_texts.assert_called_once()
        mock_vectorstore.add_documents.assert_called_once()

@pytest.mark.asyncio
async def test_ingest_txt_success(mock_vectorstore, mock_embedding_service):
    with patch("app.services.ingestion.extract_text_from_txt") as mock_extract, \
         patch("app.services.ingestion.chunk_text") as mock_chunk:
        
        mock_extract.return_value = "Mocked TXT content"
        mock_chunk.return_value = [{"text": "Mocked TXT content", "chunk_index": 0, "start_token": 0, "end_token": 10}]
        
        result = await ingestion_service.ingest(b"content", "test.txt")
        
        assert result["status"] == "ingested"
        
        mock_extract.assert_called_once()
        mock_vectorstore.clear.assert_called_once()

@pytest.mark.asyncio
async def test_ingest_unsupported_file():
    with pytest.raises(ValueError, match="Unsupported file type"):
        await ingestion_service.ingest(b"content", "test.jpg")
