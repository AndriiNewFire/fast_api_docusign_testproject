from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200


def test_read_main_fail():
    response = client.get("/rubbish")
    assert response.status_code == 404


