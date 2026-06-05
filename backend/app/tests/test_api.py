from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_create_matter():
    response = client.post("/api/matters", json={
        "title": "Test Matter",
        "description": "A test matter"
    })
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["title"] == "Test Matter"
