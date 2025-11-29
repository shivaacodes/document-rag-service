import pytest
from unittest.mock import patch, MagicMock
from app.services.retrieval import retrieve_relevant_chunks

@pytest.mark.asyncio
async def test_retrieve_relevant_chunks_success(mock_embedding_service):
    with patch("app.services.retrieval.vectorstore") as mock_vs:
        # Setup mock return for vectorstore query
        mock_vs.collection.query.return_value = {
            "documents": [["Chunk 1", "Chunk 2"]],
            "metadatas": [[{"source": "doc1"}, {"source": "doc1"}]],
            "distances": [[0.1, 0.2]]
        }
        
        results = await retrieve_relevant_chunks("test query")
        
        assert len(results) == 2
        assert results[0]["text"] == "Chunk 1"
        assert results[0]["score"] == 0.1
        
        mock_embedding_service.embed_texts.assert_called_once()
        mock_vs.collection.query.assert_called_once()

@pytest.mark.asyncio
async def test_retrieve_empty_query():
    results = await retrieve_relevant_chunks("")
    assert results == []
