"""Health endpoint tests."""
from fastapi.testclient import TestClient
from typing import Dict, Any

def test_health_endpoint(client: TestClient) -> None:
    response = client.get("/health/")
    assert response.status_code == 200
    
    data: Dict[str, Any] = response.json()
    assert "version" in data
    assert "model_status" in data
    assert "model_info" in data
    assert "system_info" in data
    
    system_info: Dict[str, Any] = data["system_info"]
    assert "system" in system_info
    assert "platform" in system_info["system"]
    assert "cpu_count" in system_info["system"]
    
    assert data["model_status"] == "healthy"
    
    model_info: Dict[str, Any] = data["model_info"]
    assert model_info["model_name"] == "test-model"
    assert model_info["n_params"] == 7000000000
