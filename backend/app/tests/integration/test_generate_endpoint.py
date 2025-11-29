import pytest
from httpx import AsyncClient
from unittest.mock import patch

@pytest.mark.asyncio
async def test_generate_endpoint_success(client: AsyncClient):
    with patch("app.api.routes_generate.generate_answer") as mock_generate, \
         patch("app.api.routes_generate.retrieve_relevant_chunks") as mock_retrieve:
        
        mock_retrieve.return_value = [{"text": "Chunk 1", "score": 0.1, "metadata": {}}]
        mock_generate.return_value = "Generated Answer"
        
        response = await client.post(
            "/api/generate", 
            json={"query": "test query"},
            headers={"X-API-Key": "local-dev-key"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["answer"] == "Generated Answer"
        assert response.status_code == 200
        data = response.json()
        assert data["answer"] == "Generated Answer"
        assert len(data["chunks"]) == 1
        
        mock_retrieve.assert_called_once()
        mock_generate.assert_called_once()

