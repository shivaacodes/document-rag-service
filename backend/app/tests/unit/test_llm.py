import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from app.services.llm import generate_answer

@pytest.mark.asyncio
async def test_generate_answer_success():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"response": "Generated answer"}
    
    # Mock httpx.AsyncClient context manager
    mock_client = AsyncMock()
    mock_client.post.return_value = mock_response
    
    with patch("app.services.llm.httpx.AsyncClient") as MockClient:
        MockClient.return_value.__aenter__.return_value = mock_client
        
        answer = await generate_answer("query", [{"text": "context"}])
        
        assert answer == "Generated answer"

@pytest.mark.asyncio
async def test_generate_answer_fallback_on_error():
    # Mock httpx.AsyncClient to raise exception
    with patch("app.services.llm.httpx.AsyncClient") as MockClient:
        MockClient.return_value.__aenter__.side_effect = Exception("Connection error")
        
        answer = await generate_answer("query", [{"text": "context"}])
        
        assert "Fallback Mode" in answer
        assert "context" in answer
