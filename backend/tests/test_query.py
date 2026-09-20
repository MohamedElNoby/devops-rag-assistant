import pytest
from fastapi.testclient import TestClient
from app.main import app

def test_health_check():
    """Verify that the health check endpoint returns 200 OK."""
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

def test_query_success():
    """Verify standard query execution returns valid answer and sources."""
    # Using 'with TestClient(app)' triggers the FastAPI lifespan startup events
    with TestClient(app) as client:
        payload = {"question": "What is Docker?"}
        response = client.post("/query", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert isinstance(data["sources"], list)
        assert len(data["answer"]) > 0

def test_query_validation_error():
    """Verify invalid input triggers a 422 Unprocessable Entity error."""
    with TestClient(app) as client:
        payload = {"question": ""}
        response = client.post("/query", json=payload)
        assert response.status_code == 422