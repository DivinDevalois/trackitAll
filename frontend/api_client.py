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


def update_task(task_id: int, *, title: str, description: str | None) -> dict:
    payload: dict = {"title": title, "description": description or ""}
    response = requests.patch(f"{API_BASE_URL}/tasks/{task_id}", json=payload)
    response.raise_for_status()
    return response.json()


def delete_task(task_id: int) -> None:
    response = requests.delete(f"{API_BASE_URL}/tasks/{task_id}")
    response.raise_for_status()


def list_habits() -> list[dict]:
    response = requests.get(f"{API_BASE_URL}/habits")
    response.raise_for_status()
    return response.json()


def create_habit(
    *,
    name: str,
    target_frequency_per_week: int,
    description: str | None = None,
    type: str = "build",
    target_time: str | None = None,
) -> dict:
    payload: dict = {
        "name": name,
        "target_frequency_per_week": target_frequency_per_week,
        "type": type,
    }
    if description:
        payload["description"] = description
    if target_time:
        payload["target_time"] = target_time
    response = requests.post(f"{API_BASE_URL}/habits", json=payload)
    response.raise_for_status()
    return response.json()


def delete_habit(habit_id: int) -> None:
    response = requests.delete(f"{API_BASE_URL}/habits/{habit_id}")
    response.raise_for_status()


def set_habit_active(habit_id: int, is_active: bool) -> dict:
    response = requests.patch(f"{API_BASE_URL}/habits/{habit_id}", json={"is_active": is_active})
    response.raise_for_status()
    return response.json()


def check_in_habit(
    habit_id: int,
    check_in_date: str,
    *,
    completed: bool = True,
    duration_minutes: int | None = None,
) -> dict:
    payload: dict = {"date": check_in_date, "completed": completed}
    if duration_minutes is not None:
        payload["duration_minutes"] = duration_minutes
    response = requests.post(f"{API_BASE_URL}/habits/{habit_id}/check-in", json=payload)
    response.raise_for_status()
    return response.json()


def list_projects() -> list[dict]:
    response = requests.get(f"{API_BASE_URL}/projects")
    response.raise_for_status()
    return response.json()


def create_project(*, name: str, description: str | None = None) -> dict:
    payload: dict = {"name": name}
    if description:
        payload["description"] = description
    response = requests.post(f"{API_BASE_URL}/projects", json=payload)
    response.raise_for_status()
    return response.json()


def update_project(project_id: int, *, name: str | None = None, status: str | None = None) -> dict:
    payload: dict = {}
    if name is not None:
        payload["name"] = name
    if status is not None:
        payload["status"] = status
    response = requests.patch(f"{API_BASE_URL}/projects/{project_id}", json=payload)
    response.raise_for_status()
    return response.json()


def delete_project(project_id: int) -> None:
    response = requests.delete(f"{API_BASE_URL}/projects/{project_id}")
    response.raise_for_status()


def list_transactions() -> list[dict]:
    response = requests.get(f"{API_BASE_URL}/transactions")
    response.raise_for_status()
    return response.json()


def create_transaction(
    *,
    date: str,
    amount: str,
    type: str,
    category: str,
    description: str | None = None,
) -> dict:
    payload: dict = {"date": date, "amount": amount, "type": type, "category": category}
    if description:
        payload["description"] = description
    response = requests.post(f"{API_BASE_URL}/transactions", json=payload)
    response.raise_for_status()
    return response.json()


def delete_transaction(transaction_id: int) -> None:
    response = requests.delete(f"{API_BASE_URL}/transactions/{transaction_id}")
    response.raise_for_status()


def get_finance_metrics(category: str | None = None) -> list[dict]:
    params = {"category": category} if category is not None else {}
    response = requests.get(f"{API_BASE_URL}/analytics/finances", params=params)
    response.raise_for_status()
    return response.json()


def get_finance_balance() -> dict:
    response = requests.get(f"{API_BASE_URL}/analytics/finances/balance")
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


def get_habit_task_correlation(window_days: int = 30) -> dict:
    response = requests.get(
        f"{API_BASE_URL}/analytics/correlation", params={"window_days": window_days}
    )
    response.raise_for_status()
    return response.json()


def get_habit_streaks() -> list[dict]:
    response = requests.get(f"{API_BASE_URL}/analytics/streaks")
    response.raise_for_status()
    return response.json()
