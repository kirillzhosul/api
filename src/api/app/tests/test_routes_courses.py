"""
    Tests courses API methods.
"""

import pytest
from app.app import app
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """Web server application fixture to have app initialized."""
    with TestClient(app) as c:
        yield c


def test_read_courses_list(client):  # pylint: disable=redefined-outer-name
    """Tests that server responds with blank courses list for list courses method."""
    response = client.get("/courses/list?page=1&per_page=5")
    assert response.status_code == 200

    json = response.json()
    assert "success" in json
    assert "v" in json
    assert "courses" in json["success"]
    assert "current_total" in json["success"]
    assert "pagination" in json["success"]
    assert "total" in json["success"]["pagination"]
    assert "page" in json["success"]["pagination"]
    assert "per_page" in json["success"]["pagination"]
    assert "max_page" in json["success"]["pagination"]
    assert json["success"]["pagination"]["page"] == 1
    assert json["success"]["pagination"]["per_page"] == 5
    assert json["success"]["current_total"] == 0
