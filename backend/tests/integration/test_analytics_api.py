from datetime import date

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


def test_task_metrics_reflects_created_and_completed_tasks(client):
    today = date.today().isoformat()

    first = client.post("/tasks", json={"title": "A"}).json()
    client.post("/tasks", json={"title": "B"})
    client.patch(f"/tasks/{first['id']}/status", json={"status": "done"})

    response = client.get("/analytics/tasks")

    assert response.status_code == 200
    today_row = next(row for row in response.json() if row["day"] == today)
    assert today_row["tasks_created"] == 2
    assert today_row["tasks_completed"] == 1


def test_habit_metrics_returns_check_ins(client):
    habit = client.post("/habits", json={"name": "Gym"}).json()
    client.post(f"/habits/{habit['id']}/check-in", json={"date": "2026-07-20", "completed": True})
    client.post(f"/habits/{habit['id']}/check-in", json={"date": "2026-07-21", "completed": False})

    response = client.get("/analytics/habits")

    assert response.status_code == 200
    body = response.json()
    assert body == [
        {"habit_id": habit["id"], "habit_name": "Gym", "day": "2026-07-20", "completed": True},
        {"habit_id": habit["id"], "habit_name": "Gym", "day": "2026-07-21", "completed": False},
    ]


def test_habit_metrics_can_be_filtered_by_habit_id(client):
    gym = client.post("/habits", json={"name": "Gym"}).json()
    reading = client.post("/habits", json={"name": "Read"}).json()
    client.post(f"/habits/{gym['id']}/check-in", json={"date": "2026-07-20"})
    client.post(f"/habits/{reading['id']}/check-in", json={"date": "2026-07-20"})

    response = client.get(f"/analytics/habits?habit_id={gym['id']}")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["habit_id"] == gym["id"]


def test_correlation_reflects_todays_habits_and_tasks(client):
    today = date.today().isoformat()

    habit = client.post("/habits", json={"name": "Gym"}).json()
    client.post(f"/habits/{habit['id']}/check-in", json={"date": today})

    t1 = client.post("/tasks", json={"title": "A"}).json()
    t2 = client.post("/tasks", json={"title": "B"}).json()
    client.patch(f"/tasks/{t1['id']}/status", json={"status": "done"})
    client.patch(f"/tasks/{t2['id']}/status", json={"status": "done"})

    response = client.get("/analytics/correlation?window_days=1")

    assert response.status_code == 200
    body = response.json()
    assert body["days"] == [
        {"day": today, "tasks_completed": 2, "habit_completion_rate": 1.0}
    ]
    assert body["avg_tasks_completed_on_good_habit_days"] == 2.0
    assert body["avg_tasks_completed_on_bad_habit_days"] is None


def test_finance_metrics_aggregates_by_day_and_category(client):
    client.post(
        "/transactions",
        json={"date": "2026-07-20", "amount": "2000", "type": "income", "category": "Salaire"},
    )
    client.post(
        "/transactions",
        json={"date": "2026-07-20", "amount": "30.50", "type": "expense", "category": "Alimentation"},
    )
    client.post(
        "/transactions",
        json={"date": "2026-07-20", "amount": "15", "type": "expense", "category": "Alimentation"},
    )

    response = client.get("/analytics/finances")

    assert response.status_code == 200
    body = response.json()
    alimentation = next(row for row in body if row["category"] == "Alimentation")
    assert alimentation["expense"] == "45.50"
    assert alimentation["income"] == "0.00"


def test_finance_metrics_can_be_filtered_by_category(client):
    client.post(
        "/transactions",
        json={"date": "2026-07-20", "amount": "2000", "type": "income", "category": "Salaire"},
    )
    client.post(
        "/transactions",
        json={"date": "2026-07-20", "amount": "30", "type": "expense", "category": "Alimentation"},
    )

    response = client.get("/analytics/finances?category=Salaire")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["category"] == "Salaire"
