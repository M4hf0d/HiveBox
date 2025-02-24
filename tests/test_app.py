import pytest
from app import app


@pytest.fixture
def client():
    """Create a test client for the app."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_version_endpoint(client):
    """Test the /version endpoint returns correct version."""
    response = client.get("/version")
    assert response.status_code == 200
    assert response.data.decode("utf-8") == "<p>v0.0.1</p>"
