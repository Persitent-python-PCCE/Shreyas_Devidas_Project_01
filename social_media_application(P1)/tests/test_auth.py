def test_registration(client):

    response = client.post(
        "/api/register",
        json={
            "username": "pytest_user_04",
            "email": "pytest_user_04@gmail.com",
            "password": "test123"
        }
    )

    print(response.status_code)
    print(response.get_json())

    assert response.status_code in [200, 201]

    data = response.get_json()

    assert data["success"] is True


def test_login(client):

    response = client.post(
        "/api/login",
        json={
            "email": "pytest_user_04@gmail.com",
            "password": "test123"
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True


def test_wrong_password(client):

    response = client.post(
        "/api/login",
        json={
            "email": "pytest_user_04@gmail.com",
            "password": "wrongpassword"
        }
    )

    assert response.status_code in [400, 401]

    data = response.get_json()

    assert data["success"] is False


def test_login_non_existing_user(client):

    response = client.post(
        "/api/login",
        json={
            "email": "doesnotexist@gmail.com",
            "password": "wrong123"
        }
    )

    assert response.status_code in [400, 401, 404]

    data = response.get_json()

    assert data["success"] is False