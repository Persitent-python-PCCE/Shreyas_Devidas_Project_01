def test_like_post(client):

    login_response = client.post(
        "/api/login",
        json={
            "email": "pytest_user_01@gmail.com",
            "password": "test123"
        }
    )

    token = login_response.get_json()["access_token"]

    response = client.post(
        "/api/posts/1/like",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code in [200, 201]

    data = response.get_json()

    assert data["success"] is True


def test_unlike_post(client):

    login_response = client.post(
        "/api/login",
        json={
            "email": "pytest_user_01@gmail.com",
            "password": "test123"
        }
    )

    token = login_response.get_json()["access_token"]

    response = client.delete(
        "/api/posts/1/like",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code in [200, 204]

    if response.data:
        data = response.get_json()

        assert data["success"] is True

def test_add_comment(client):

    login_response = client.post(
        "/api/login",
        json={
            "email": "pytest_user_01@gmail.com",
            "password": "test123"
        }
    )

    token = login_response.get_json()["access_token"]

    response = client.post(
        "/api/posts/1/comments",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "content": "This is a pytest comment"
        }
    )

    assert response.status_code in [200, 201]

    data = response.get_json()

    assert data["success"] is True

    