"""Dependency-upgrade contracts for both existing FastAPI entry points."""

import pytest
from fastapi.testclient import TestClient

import api
import service


@pytest.fixture
def service_client():
    service.reset_game_state()
    with TestClient(service.app) as client:
        yield client
    service.reset_game_state()


@pytest.fixture
def session_client():
    api.sessions.clear()
    with TestClient(api.app) as client:
        yield client
    api.sessions.clear()


def test_service_state_round_trip(service_client):
    assert service_client.get("/status").json()["player"]["credits"] == 1000
    travel = service_client.post("/travel", json={"sector": 2})
    assert travel.status_code == 200
    assert travel.json()["player"]["current_sector"] == 2
    assert travel.json()["player"]["fuel"] == 90
    for action, credits in [("buy", 950), ("sell", 1000)]:
        response = service_client.post(
            "/trade", json={"item": "Food", "quantity": 1, "trade_action": action}
        )
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert response.json()["credits"] == credits
    assert service.game_state["inventory"] == []


@pytest.mark.parametrize("path,payload,field", [
    ("/travel", {}, "sector"),
    ("/travel", {"sector": "invalid"}, "sector"),
    ("/trade", {"item": "Food", "quantity": 1.5, "trade_action": "buy"}, "quantity"),
])
def test_validation_does_not_mutate_state(service_client, path, payload, field):
    response = service_client.post(path, json=payload)
    assert response.status_code == 422
    assert any(error["loc"] == ["body", field] for error in response.json()["detail"])
    assert service.game_state == service._default_state()


def test_malformed_json_and_method_routing(service_client):
    response = service_client.post(
        "/travel", content="{broken", headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "json_invalid"
    assert service_client.get("/travel").status_code == 405
    assert service_client.get("/missing").status_code == 404
    assert service.game_state == service._default_state()


def test_session_header_authentication_and_isolation(session_client):
    assert session_client.get("/api/status").status_code == 422
    invalid = session_client.get("/api/status", headers={"X-Token": "invalid"})
    assert invalid.status_code == 401
    assert invalid.json() == {"detail": "Invalid or expired session"}
    tokens = []
    for _ in range(2):
        response = session_client.post("/api/session")
        assert response.status_code == 200
        tokens.append(response.json()["token"])
    assert tokens[0] != tokens[1]
    api.sessions[tokens[0]]["player"].credits = 123
    for token, credits in [(tokens[0], 123), (tokens[1], 1000)]:
        response = session_client.get("/api/status", headers={"X-Token": token})
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert response.json()["player"]["credits"] == credits
        assert isinstance(response.json()["world"]["discovered_sectors"], list)


@pytest.mark.parametrize("app,paths", [
    (service.app, {"/status", "/travel", "/trade"}),
    (api.app, {"/api/session", "/api/status", "/api/travel", "/api/trade"}),
])
def test_openapi_and_documentation(app, paths):
    with TestClient(app) as client:
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert paths <= schema["paths"].keys()
        assert schema["components"]["schemas"]["TravelRequest"]["properties"]["sector"]["type"] == "integer"
        assert client.get("/docs").status_code == 200
