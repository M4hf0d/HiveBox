import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import requests
import pytest

BASE_URL = "http://localhost:5000"


@pytest.mark.integration
def test_temperature_status():
    response = requests.get(f"{BASE_URL}/temperature")
    assert response.status_code in [200, 404]  # 404 if no data
    if response.status_code == 200:
        data = response.json()
        assert "average_temperature" in data
        assert "status" in data
        temp = data["average_temperature"]
        if temp < 10:
            assert data["status"] == "Too Cold"
        elif 11 <= temp <= 36:
            assert data["status"] == "Good"
        else:
            assert data["status"] == "Too Hot"


@pytest.mark.integration
def test_metrics_endpoint():
    response = requests.get(f"{BASE_URL}/metrics")
    assert response.status_code == 200
    assert "hivebox_requests_total" in response.text