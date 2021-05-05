from fastapi.testclient import TestClient
import main

client = TestClient(main.app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200


def test_read_main_fail():
    response = client.get("/rubbish")
    assert response.status_code == 404


