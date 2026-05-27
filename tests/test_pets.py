import os

os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from app import create_app


def test_health():
    app = create_app()
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json == {"status": "ok"}


def test_create_pet():
    app = create_app()
    client = app.test_client()

    response = client.post(
        "/pets",
        json={
            "name": "Milo",
            "species": "Dog",
            "age": 5
        }
    )

    assert response.status_code == 200
    assert response.json["name"] == "Milo"
    assert response.json["species"] == "Dog"
    assert response.json["age"] == 5