from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_returns_24_predictions():
    payload = {"series": [3.2] * 48}
    r = client.post("/forecast", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "prediction" in data
    assert isinstance(data["prediction"], list)
    assert len(data["prediction"]) == 24

def test_invalid_payload_returns_error():
    # strings force validation/model failure
    payload = {"series": ["not-a-number"] * 48}
    r = client.post("/forecast", json=payload)
    # Pydantic may catch it (422) or your try/except might return 400
    assert r.status_code in (400, 422)
