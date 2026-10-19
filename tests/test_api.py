from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200 and r.json()["status"] == "ok"

def test_invalid_ticket_rejected():
    r = client.post("/tickets/analyze", json={"title": "x", "description": "y"})
    assert r.status_code == 422
