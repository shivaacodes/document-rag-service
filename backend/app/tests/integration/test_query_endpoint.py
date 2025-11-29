import pytest
from httpx import AsyncClient
from unittest.mock import patch

@pytest.mark.asyncio
async def test_query_endpoint_success(client: AsyncClient):
    with patch("app.api.routes_query.retrieve_relevant_chunks") as mock_retrieve:
        mock_retrieve.return_value = [{"text": "Chunk 1", "score": 0.1, "metadata": {}}]
        
        response = await client.post(
            "/api/query", 
            json={"query": "test query"},
            headers={"X-API-Key": "local-dev-key"}
        )
        
        assert response.status_code == 200
        assert len(response.json()["results"]) == 1
        mock_retrieve.assert_called_once()
