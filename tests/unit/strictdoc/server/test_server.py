from fastapi.testclient import TestClient

from strictdoc.server.main import create_app


def test_server_01():
    client = TestClient(create_app(None))
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_server_02():
    expected_json = {
        'requirements':
            [
                {'statement': 'System shall do 1', 'title': 'Requirement 1'},
                {'statement': 'System shall do 2', 'title': 'Requirement 2'},
                {'statement': 'System shall do 3', 'title': 'Requirement 3'}
            ]
    }
    client = TestClient(create_app(None))
    response = client.get("/requirements")
    assert response.status_code == 200
    assert response.json() == expected_json
