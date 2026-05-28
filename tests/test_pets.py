import os

os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["JWT_SECRET_KEY"] = "test-secret"

from app import create_app


def test_health():
    app = create_app()
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json == {"status": "ok"}


def test_create_pet_with_jwt():
    app = create_app()
    client = app.test_client()

    client.post(
        "/register",
        json={
            "username": "testuser",
            "password": "123456"
        }
    )

    login_response = client.post(
        "/login",
        json={
            "username": "testuser",
            "password": "123456"
        }
    )

    token = login_response.json["access_token"]

    response = client.post(
        "/pets",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "name": "Milo",
            "species": "Dog",
            "age": 5
        }
    )

    assert response.status_code == 200
    assert response.json["name"] == "Milo"