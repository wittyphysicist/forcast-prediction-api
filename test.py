from fastapi.testclient import TestClient
import pytest
from main import app


@pytest.fixture
def client():
    return TestClient(app)


def _series(n=48):
    return [3.0 + 0.01 * (i % 24) + 0.001 * i for i in range(n)]


def test_forecast(client):
    payload = {"series": _series(48)} # checks if 48 data points return 24 data points
    r = client.post("/forecast", json=payload)

    assert r.status_code == 200
    data = r.json()
    assert "prediction" in data

    pred = data["prediction"]
    assert isinstance(pred, list)
    assert len(pred) == 24
    assert all(isinstance(x, (int, float)) for x in pred)


def test_short_series_400(client):
    payload = {"series": _series(10)}  # too short for 24 points
    r = client.post("/forecast", json=payload)

    assert r.status_code == 400
    # Helpful error message makes debugging easier
    assert "48" in r.json().get("detail", "")


@pytest.mark.parametrize(
    "bad_payload",
    [
        {"series": ["not-a-number"] * 48},  # wrong element type
        {"series": "not-a-list"},           # wrong shape
        {},                                 # missing required field
    ],
)
def test_schema_validation_422_for_bad_json(client, bad_payload):
    r = client.post("/forecast", json=bad_payload)
    assert r.status_code == 422

