"""Exercise the Flask stack against a temporary database, never player data."""

import importlib
from unittest.mock import patch

import pytest


@pytest.fixture(scope="module")
def web_app(tmp_path_factory):
    from web import models

    database = tmp_path_factory.mktemp("web-compatibility") / "test.db"
    initialize = models.init_database

    def initialize_test_database(app, **kwargs):
        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{database}"
        initialize(app, enable_local_fallback=False)

    with patch.object(models, "init_database", initialize_test_database):
        module = importlib.import_module("web.app")
    module.app.config["TESTING"] = True
    yield module.app
    with module.app.app_context():
        models.db.session.remove()
        models.db.engine.dispose()


def test_templates_and_static_assets(web_app):
    client = web_app.test_client()
    for path in ("/", "/game", "/manifest.json", "/service-worker.js"):
        response = client.get(path)
        assert response.status_code == 200
        assert response.headers["X-Content-Type-Options"] == "nosniff"


def test_session_creation_reuse_and_isolation(web_app):
    client = web_app.test_client()
    first = client.post("/api/session", json={})
    assert first.status_code == 200
    data = first.get_json()
    assert data["success"] and data["token"] and data["csrf_token"]
    assert "Cookie" in first.vary
    second = client.post("/api/session", json={}).get_json()
    assert second == data
    other = web_app.test_client().post("/api/session", json={}).get_json()
    assert other["token"] != data["token"]
    assert other["csrf_token"] != data["csrf_token"]


def test_status_after_session_creation(web_app):
    client = web_app.test_client()
    assert client.post("/api/session", json={}).status_code == 200
    response = client.get("/api/status")
    assert response.status_code == 200
    assert response.get_json()["success"]


def test_registration_login_and_logout(web_app):
    client = web_app.test_client()
    credentials = {
        "username": "dependency_test",
        "password": "test-only-password",
        "email": "dependency-test@example.invalid",
    }
    registered = client.post("/api/auth/register", json=credentials)
    assert registered.status_code == 200
    assert registered.get_json()["success"]
    assert client.post("/api/auth/logout", json={}).get_json()["success"]
    assert (
        client.post(
            "/api/auth/login", json={**credentials, "password": "incorrect"}
        ).status_code
        == 401
    )
    logged_in = client.post("/api/auth/login", json=credentials)
    assert logged_in.status_code == 200
    assert logged_in.get_json()["user_id"] == registered.get_json()["user_id"]
    assert client.post("/api/auth/logout", json={}).get_json()["success"]
    with client.session_transaction() as session:
        assert not session


def test_csrf_validation_is_preserved(web_app):
    client = web_app.test_client()
    session = client.post("/api/session", json={}).get_json()
    assert client.post("/api/save", json={}).status_code == 403
    assert (
        client.post(
            "/api/save", json={}, headers={"X-CSRF-Token": "incorrect"}
        ).status_code
        == 403
    )
    # A valid token reaches input validation without writing a save file.
    response = client.post(
        "/api/save",
        json={"save_name": ""},
        headers={"X-CSRF-Token": session["csrf_token"]},
    )
    assert response.status_code == 400
    assert response.get_json()["message"] == "Invalid save name"
