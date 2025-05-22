"""Chat endpoint tests."""
from unittest.mock import patch
from fastapi.testclient import TestClient
from typing import Dict, Any
from app.tests.utils.mock_llm import MockLLM

def test_chat_model_info_endpoint(client: TestClient) -> None:
    response = client.get("/chat/model-info")
    assert response.status_code == 200
    
    data: Dict[str, Any] = response.json()
    assert data["status"] == "success"
    assert "data" in data
    
    model_data: Dict[str, Any] = data["data"]
    assert "model_name" in model_data
    assert "n_params" in model_data
    assert model_data["model_name"] == "test-model"

def test_chat_endpoint_validation(client: TestClient) -> None:
    # Missing 'messages' field
    response = client.post("/chat/", json={})
    assert response.status_code == 422
    
    # Empty messages list
    response = client.post("/chat/", json={"messages": []})
    assert response.status_code == 200
    
    # Invalid role
    response = client.post("/chat/", json={
        "messages": [{"role": "invalid_role", "content": "Hello"}]
    })
    assert response.status_code == 422
    
    # Valid message structure
    response = client.post("/chat/", json={
        "messages": [{"role": "user", "content": "Hello"}]
    })
    assert response.status_code == 200

def test_chat_endpoint_with_valid_message(client: TestClient) -> None:
    with patch('app.services.llm_service.llm_service.get_llm_response_stream') as mock_stream:
        mock_stream.return_value = MockLLM.get_mock_stream()
        
        response = client.post("/chat/", json={
            "messages": [{"role": "user", "content": "Hello"}]
        })
        assert response.status_code == 200
        
        assert "text/event-stream" in response.headers["content-type"]
        assert mock_stream.called
