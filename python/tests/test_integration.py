import pytest
from flask.testing import FlaskClient

from mines import create_app


@pytest.fixture
def client() -> FlaskClient:
    """Provides a new client for each test case that needs it."""
    app = create_app()
    with app.test_client() as client:
        with app.app_context():
            yield client


def test_create_game(client: FlaskClient):
    result = client.post("/games", json={"width": 5, "height": 6, "numberOfMines": 7})
    assert result.is_json
    assert "id" in result.json


def test_uncover_tile(client: FlaskClient):
    create_response = client.post("/games", json={"width": 3, "height": 3, "numberOfMines": 3})
    game_id = create_response.json["id"]
    result = client.post(f"/games/{game_id}/guesses", json={"x": 1, "y": 2})
    assert result.is_json
    assert "result" in result.json
