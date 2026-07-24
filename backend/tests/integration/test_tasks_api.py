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


def test_create_task_returns_201_with_defaults(client):
    response = client.post("/tasks", json={"title": "Write the API"})

    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Write the API"
    assert body["status"] == "todo"
    assert body["priority"] == "medium"
    assert body["id"] is not None


def test_create_task_missing_title_returns_422(client):
    response = client.post("/tasks", json={"description": "no title"})

    assert response.status_code == 422


def test_list_tasks_returns_created_tasks(client):
    client.post("/tasks", json={"title": "First"})
    client.post("/tasks", json={"title": "Second"})

    response = client.get("/tasks")

    assert response.status_code == 200
    titles = [task["title"] for task in response.json()]
    assert titles == ["First", "Second"]


def test_get_task_returns_task(client):
    created = client.post("/tasks", json={"title": "Find me"}).json()

    response = client.get(f"/tasks/{created['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_task_returns_404_for_unknown_id(client):
    response = client.get("/tasks/999")

    assert response.status_code == 404


def test_update_task_status_returns_200(client):
    created = client.post("/tasks", json={"title": "To be updated"}).json()

    response = client.patch(f"/tasks/{created['id']}/status", json={"status": "done"})

    assert response.status_code == 200
    assert response.json()["status"] == "done"


def test_update_task_status_returns_404_for_unknown_id(client):
    response = client.patch("/tasks/999/status", json={"status": "done"})

    assert response.status_code == 404


def test_update_task_status_invalid_status_returns_422(client):
    created = client.post("/tasks", json={"title": "Invalid status"}).json()

    response = client.patch(f"/tasks/{created['id']}/status", json={"status": "not_a_status"})

    assert response.status_code == 422


def test_create_task_with_project_id_returns_201(client):
    project = client.post("/projects", json={"name": "TrackItAll"}).json()

    response = client.post(
        "/tasks", json={"title": "Ship TIA-21", "project_id": project["id"]}
    )

    assert response.status_code == 201
    assert response.json()["project_id"] == project["id"]


def test_create_task_with_unknown_project_id_returns_400(client):
    response = client.post("/tasks", json={"title": "Orphan", "project_id": 999})

    assert response.status_code == 400


def test_list_tasks_can_be_filtered_by_project_id(client):
    project = client.post("/projects", json={"name": "TrackItAll"}).json()
    client.post("/tasks", json={"title": "In project", "project_id": project["id"]})
    client.post("/tasks", json={"title": "Not in project"})

    response = client.get(f"/tasks?project_id={project['id']}")

    assert response.status_code == 200
    titles = [task["title"] for task in response.json()]
    assert titles == ["In project"]
