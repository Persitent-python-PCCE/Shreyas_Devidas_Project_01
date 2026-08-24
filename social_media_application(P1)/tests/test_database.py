def test_user_saved_in_database(client):

    from models.user import User

    email = "database_test100@gmail.com"

    response = client.post(
        "/api/register",
        json={
            "username": "database_test100",
            "email": email,
            "password": "test123"
        }
    )

    assert response.status_code in [200, 201]

    user = User.query.filter_by(
        email=email
    ).first()

    assert user is not None

    assert user.email == email