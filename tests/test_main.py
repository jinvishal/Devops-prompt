from fastapi.testclient import TestClient

def test_read_root(client: TestClient):
    """
    Test that the root endpoint is accessible.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Education Platform API. Visit /docs for documentation."}
