from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_status():
    response = client.get("/router/status")
    assert response.status_code == 200
