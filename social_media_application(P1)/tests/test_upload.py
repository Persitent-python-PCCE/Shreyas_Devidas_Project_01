from io import BytesIO


def test_invalid_image_upload(client):

    login_response = client.post(
        "/api/login",
        json={
            "email": "pytest_user_01@gmail.com",
            "password": "test123"
        }
    )

    token = login_response.get_json()["access_token"]

    response = client.post(
        "/api/posts",
        headers={
            "Authorization": f"Bearer {token}"
        },
        data={
            "content": "Invalid file test",

            "image": (
                BytesIO(b"fake file"),
                "test.exe"
            )
        },
        content_type="multipart/form-data"
    )

    assert response.status_code in [400, 415]


def test_valid_image_upload(client):

    login_response = client.post(
        "/api/login",
        json={
            "email": "pytest_user_01@gmail.com",
            "password": "test123"
        }
    )

    token = login_response.get_json()["access_token"]

    response = client.post(
        "/api/posts",
        headers={
            "Authorization": f"Bearer {token}"
        },
        data={
            "content": "Valid image test",

            "image": (
                BytesIO(b"\x89PNG\r\n\x1a\n"),
                "test.png"
            )
        },
        content_type="multipart/form-data"
    )

    assert response.status_code in [200, 201]