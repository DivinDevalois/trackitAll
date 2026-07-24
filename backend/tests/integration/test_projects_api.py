import pytest
from fastapi.testclient import TestClient

from app.db.session import get_session
from app.main import app


@pytest.fixture()
def client(db_session):
    def override_get_session():
        yield db_session

    app.dependency_overrides[get_session] = override_get_session
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_create_project_returns_201(client):
    response = client.post("/projects", json={"name": "TrackItAll"})

    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "TrackItAll"
    assert body["description"] is None
    assert body["id"] is not None


def test_create_project_missing_name_returns_422(client):
    response = client.post("/projects", json={"description": "no name"})

    assert response.status_code == 422


def test_list_projects_returns_created_projects(client):
    client.post("/projects", json={"name": "First"})
    client.post("/projects", json={"name": "Second"})

    response = client.get("/projects")

    assert response.status_code == 200
    names = [project["name"] for project in response.json()]
    assert names == ["First", "Second"]


def test_get_project_returns_project(client):
    created = client.post("/projects", json={"name": "Find me"}).json()

    response = client.get(f"/projects/{created['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_project_returns_404_for_unknown_id(client):
    response = client.get("/projects/999")

    assert response.status_code == 404


def test_update_project_changes_name(client):
    created = client.post("/projects", json={"name": "Old name"}).json()

    response = client.patch(f"/projects/{created['id']}", json={"name": "New name"})

    assert response.status_code == 200
    assert response.json()["name"] == "New name"


def test_update_project_returns_404_for_unknown_id(client):
    response = client.patch("/projects/999", json={"name": "Whatever"})

    assert response.status_code == 404


def test_delete_project_returns_204(client):
    created = client.post("/projects", json={"name": "To delete"}).json()

    response = client.delete(f"/projects/{created['id']}")

    assert response.status_code == 204
    assert client.get(f"/projects/{created['id']}").status_code == 404


def test_delete_project_returns_404_for_unknown_id(client):
    response = client.delete("/projects/999")

    assert response.status_code == 404
