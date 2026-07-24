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


def test_create_transaction_returns_201(client):
    response = client.post(
        "/transactions",
        json={"date": "2026-07-24", "amount": "42.50", "type": "expense", "category": "Alimentation"},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["category"] == "Alimentation"
    assert body["type"] == "expense"
    assert float(body["amount"]) == 42.5


def test_create_transaction_negative_amount_returns_422(client):
    response = client.post(
        "/transactions",
        json={"date": "2026-07-24", "amount": "-5", "type": "expense", "category": "Alimentation"},
    )

    assert response.status_code == 422


def test_create_transaction_missing_category_returns_422(client):
    response = client.post(
        "/transactions", json={"date": "2026-07-24", "amount": "10", "type": "income"}
    )

    assert response.status_code == 422


def test_list_transactions_returns_created_transactions(client):
    client.post(
        "/transactions",
        json={"date": "2026-07-20", "amount": "10", "type": "income", "category": "Salaire"},
    )
    client.post(
        "/transactions",
        json={"date": "2026-07-21", "amount": "5", "type": "expense", "category": "Transport"},
    )

    response = client.get("/transactions")

    assert response.status_code == 200
    categories = [t["category"] for t in response.json()]
    assert categories == ["Salaire", "Transport"]


def test_get_transaction_returns_404_for_unknown_id(client):
    response = client.get("/transactions/999")

    assert response.status_code == 404


def test_update_transaction_changes_category(client):
    created = client.post(
        "/transactions",
        json={"date": "2026-07-24", "amount": "10", "type": "expense", "category": "Old"},
    ).json()

    response = client.patch(f"/transactions/{created['id']}", json={"category": "New"})

    assert response.status_code == 200
    assert response.json()["category"] == "New"


def test_update_transaction_returns_404_for_unknown_id(client):
    response = client.patch("/transactions/999", json={"category": "Whatever"})

    assert response.status_code == 404


def test_delete_transaction_returns_204(client):
    created = client.post(
        "/transactions",
        json={"date": "2026-07-24", "amount": "10", "type": "expense", "category": "To delete"},
    ).json()

    response = client.delete(f"/transactions/{created['id']}")

    assert response.status_code == 204
    assert client.get(f"/transactions/{created['id']}").status_code == 404


def test_delete_transaction_returns_404_for_unknown_id(client):
    response = client.delete("/transactions/999")

    assert response.status_code == 404
