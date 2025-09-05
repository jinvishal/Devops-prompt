from fastapi.testclient import TestClient
from fastapi import status

def test_login_for_access_token_success(client: TestClient):
    """
    Test successful login and token generation.
    """
    # Step 1: Create a user to log in with
    user_data = {"email": "auth_test@example.com", "password": "a_secure_password"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201

    # Step 2: Attempt to log in
    login_data = {"username": user_data["email"], "password": user_data["password"]}
    response = client.post("/token", data=login_data)

    # Step 3: Verify successful login
    assert response.status_code == 200
    token = response.json()
    assert "access_token" in token
    assert token["token_type"] == "bearer"

def test_login_wrong_password(client: TestClient):
    """
    Test login with an incorrect password.
    """
    # Step 1: Create user
    user_data = {"email": "wrong_pass@example.com", "password": "correct_password"}
    client.post("/users/", json=user_data)

    # Step 2: Attempt login with wrong password
    login_data = {"username": user_data["email"], "password": "wrong_password"}
    response = client.post("/token", data=login_data)

    # Step 3: Verify failure
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Incorrect email or password"}

def test_login_nonexistent_user(client: TestClient):
    """
    Test login with an email that does not exist.
    """
    login_data = {"username": "nosuchuser@example.com", "password": "any_password"}
    response = client.post("/token", data=login_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
