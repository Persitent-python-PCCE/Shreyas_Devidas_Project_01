def test_protected_post_api_without_jwt(client):

    response = client.post(
        "/api/posts",
        json={
            "content": "Test"
        }
    )

    assert response.status_code in [401, 422]


def test_like_without_jwt(client):

    response = client.post(
        "/api/posts/1/like"
    )

    assert response.status_code in [401, 422]


def test_comment_without_jwt(client):

    response = client.post(
        "/api/posts/1/comments",
        json={
            "content": "Unauthorized comment"
        }
    )

    assert response.status_code in [401, 422]


def test_invalid_jwt(client):

    response = client.post(
        "/api/posts",
        headers={
            "Authorization": "Bearer invalid_token"
        },
        json={
            "content": "Invalid JWT"
        }
    )

    assert response.status_code in [401, 422]