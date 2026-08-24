def test_get_posts(client):

    response = client.get("/api/posts")

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True

    assert "posts" in data


def test_create_post(client):

    login_response = client.post(
        "/api/login",
        json={
            "email": "pytest_user_01@gmail.com",
            "password": "test123"
        }
    )

    assert login_response.status_code == 200

    login_data = login_response.get_json()

    token = login_data["access_token"]

    response = client.post(
        "/api/posts",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "content": "Pytest test post"
        }
    )

    assert response.status_code in [200, 201]

    data = response.get_json()

    assert data["success"] is True

def test_create_post_without_token(client):

    response = client.post(
        "/api/posts",
        json={
            "content": "Unauthorized post"
        }
    )

    assert response.status_code in [401, 422]

def test_invalid_api_url(client):

    response = client.get(
        "/api/this-does-not-exist"
    )

    assert response.status_code == 404