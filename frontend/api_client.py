import os

import requests

API_BASE_URL = os.environ.get("API_BASE_URL", "http://127.0.0.1:8000")


def list_tasks() -> list[dict]:
    response = requests.get(f"{API_BASE_URL}/tasks")
    response.raise_for_status()
    return response.json()


def create_task(
    *,
    title: str,
    description: str | None,
    priority: str,
    due_date: str | None,
    project_id: int | None = None,
) -> dict:
    payload: dict = {"title": title, "priority": priority}
    if description:
        payload["description"] = description
    if due_date:
        payload["due_date"] = due_date
    if project_id is not None:
        payload["project_id"] = project_id
    response = requests.post(f"{API_BASE_URL}/tasks", json=payload)
    response.raise_for_status()
    return response.json()


def update_task_status(task_id: int, status: str) -> dict:
    response = requests.patch(f"{API_BASE_URL}/tasks/{task_id}/status", json={"status": status})
    response.raise_for_status()
    return response.json()


def list_habits() -> list[dict]:
    response = requests.get(f"{API_BASE_URL}/habits")
    response.raise_for_status()
    return response.json()


def create_habit(*, name: str, target_frequency_per_week: int) -> dict:
    response = requests.post(
        f"{API_BASE_URL}/habits",
        json={"name": name, "target_frequency_per_week": target_frequency_per_week},
    )
    response.raise_for_status()
    return response.json()


def check_in_habit(habit_id: int, check_in_date: str, *, completed: bool = True) -> dict:
    response = requests.post(
        f"{API_BASE_URL}/habits/{habit_id}/check-in",
        json={"date": check_in_date, "completed": completed},
    )
    response.raise_for_status()
    return response.json()


def list_projects() -> list[dict]:
    response = requests.get(f"{API_BASE_URL}/projects")
    response.raise_for_status()
    return response.json()


def create_project(*, name: str) -> dict:
    response = requests.post(f"{API_BASE_URL}/projects", json={"name": name})
    response.raise_for_status()
    return response.json()


def get_task_metrics() -> list[dict]:
    response = requests.get(f"{API_BASE_URL}/analytics/tasks")
    response.raise_for_status()
    return response.json()


def get_habit_metrics(habit_id: int | None = None) -> list[dict]:
    params = {"habit_id": habit_id} if habit_id is not None else {}
    response = requests.get(f"{API_BASE_URL}/analytics/habits", params=params)
    response.raise_for_status()
    return response.json()
