import pytest
from fastapi.testclient import TestClient

from app.core.security import get_password_hash
from app.db.session import get_db
from app.main import app
from app.models import User


@pytest.fixture
def client(db_session):
    """A TestClient whose get_db is overridden to use the test session,
    so every endpoint talks to colab_test instead of colab."""

    def _override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()


@pytest.fixture
def seed_user(db_session):
    db_session.add(
        User(
            username="johndoe",
            email="johndoe@example.com",
            full_name="John Doe",
            hashed_password=get_password_hash("secret"),
        )
    )
    db_session.commit()


def _login(client, username, password):
    return client.post(
        "/token", data={"username": username, "password": password}
    )


def test_login_returns_a_bearer_token(client, seed_user):
    response = _login(client, "johndoe", "secret")

    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]


def test_login_rejects_wrong_password(client, seed_user):
    assert _login(client, "johndoe", "wrong").status_code == 401


def test_login_rejects_unknown_user(client):
    assert _login(client, "ghost", "secret").status_code == 401


def test_me_returns_current_user_without_password(client, seed_user):
    token = _login(client, "johndoe", "secret").json()["access_token"]

    response = client.get(
        "/users/me/", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    body = response.json()
    assert body["username"] == "johndoe"
    assert body["email"] == "johndoe@example.com"
    assert "hashed_password" not in body


def test_me_without_token_is_unauthorized(client):
    assert client.get("/users/me/").status_code == 401
