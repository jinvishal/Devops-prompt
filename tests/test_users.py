from fastapi.testclient import TestClient

def test_create_user_success(client: TestClient):
    """
    Test creating a new user successfully.
    """
    response = client.post(
        "/users/",
        json={"email": "newuser@example.com", "password": "password123"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert "id" in data
    assert "hashed_password" not in data # Ensure password is not returned

def test_create_user_duplicate_email(client: TestClient):
    """
    Test that creating a user with a duplicate email fails.
    """
    # First, create a user
    client.post(
        "/users/",
        json={"email": "duplicate@example.com", "password": "password123"},
    )

    # Then, try to create another user with the same email
    response = client.post(
        "/users/",
        json={"email": "duplicate@example.com", "password": "password456"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered"}
