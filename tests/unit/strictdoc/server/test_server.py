from fastapi.testclient import TestClient

from strictdoc.server.main import create_app


def test_server_01():
    client = TestClient(create_app(None))
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}
