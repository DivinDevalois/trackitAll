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


def test_create_habit_returns_201_with_defaults(client):
    response = client.post("/habits", json={"name": "Read 20 minutes"})

    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Read 20 minutes"
    assert body["target_frequency_per_week"] == 7


def test_create_habit_missing_name_returns_422(client):
    response = client.post("/habits", json={"target_frequency_per_week": 3})

    assert response.status_code == 422


def test_create_break_habit_with_description_and_target_time(client):
    response = client.post(
        "/habits",
        json={
            "name": "Ne pas procrastiner",
            "description": "Éviter de remettre au lendemain",
            "type": "break",
            "target_time": "09:00:00",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["type"] == "break"
    assert body["description"] == "Éviter de remettre au lendemain"
    assert body["target_time"] == "09:00:00"


def test_list_habits_returns_created_habits(client):
    client.post("/habits", json={"name": "First"})
    client.post("/habits", json={"name": "Second"})

    response = client.get("/habits")

    assert response.status_code == 200
    names = [habit["name"] for habit in response.json()]
    assert names == ["First", "Second"]


def test_get_habit_returns_404_for_unknown_id(client):
    response = client.get("/habits/999")

    assert response.status_code == 404


def test_check_in_creates_a_log(client):
    habit = client.post("/habits", json={"name": "Gym"}).json()

    response = client.post(f"/habits/{habit['id']}/check-in", json={"date": "2026-07-24"})

    assert response.status_code == 200
    body = response.json()
    assert body["habit_id"] == habit["id"]
    assert body["date"] == "2026-07-24"
    assert body["completed"] is True


def test_check_in_twice_same_day_updates_instead_of_duplicating(client):
    habit = client.post("/habits", json={"name": "Gym"}).json()

    first = client.post(f"/habits/{habit['id']}/check-in", json={"date": "2026-07-24"}).json()
    second = client.post(
        f"/habits/{habit['id']}/check-in", json={"date": "2026-07-24", "completed": False}
    ).json()

    assert first["id"] == second["id"]
    assert second["completed"] is False


def test_check_in_returns_404_for_unknown_habit(client):
    response = client.post("/habits/999/check-in", json={"date": "2026-07-24"})

    assert response.status_code == 404


def test_check_in_accepts_duration_minutes(client):
    habit = client.post("/habits", json={"name": "Gym"}).json()

    response = client.post(
        f"/habits/{habit['id']}/check-in",
        json={"date": "2026-07-24", "duration_minutes": 20},
    )

    assert response.status_code == 200
    assert response.json()["duration_minutes"] == 20


def test_update_habit_changes_fields(client):
    created = client.post("/habits", json={"name": "Old name"}).json()

    response = client.patch(f"/habits/{created['id']}", json={"name": "New name", "type": "break"})

    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "New name"
    assert body["type"] == "break"


def test_update_habit_returns_404_for_unknown_id(client):
    response = client.patch("/habits/999", json={"name": "Whatever"})

    assert response.status_code == 404


def test_delete_habit_returns_204(client):
    created = client.post("/habits", json={"name": "To delete"}).json()

    response = client.delete(f"/habits/{created['id']}")

    assert response.status_code == 204
    assert client.get(f"/habits/{created['id']}").status_code == 404


def test_delete_habit_returns_404_for_unknown_id(client):
    response = client.delete("/habits/999")

    assert response.status_code == 404
