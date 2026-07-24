from datetime import date
from decimal import Decimal

import pytest

from app.models.transaction import TransactionType
from app.repositories.transaction_repository import TransactionRepository


@pytest.fixture()
def repo(db_session):
    return TransactionRepository(db_session)


def test_create_persists_transaction(repo):
    transaction = repo.create(
        date=date(2026, 7, 24),
        amount=Decimal("42.50"),
        type=TransactionType.EXPENSE,
        category="Alimentation",
    )

    assert transaction.id is not None
    assert transaction.amount == Decimal("42.50")
    assert transaction.type == TransactionType.EXPENSE
    assert transaction.category == "Alimentation"
    assert transaction.description is None


def test_get_returns_existing_transaction(repo):
    created = repo.create(
        date=date(2026, 7, 24),
        amount=Decimal("10"),
        type=TransactionType.INCOME,
        category="Salaire",
    )

    found = repo.get(created.id)

    assert found is not None
    assert found.id == created.id


def test_get_returns_none_for_unknown_id(repo):
    assert repo.get(999) is None


def test_list_returns_all_transactions_ordered_by_date(repo):
    later = repo.create(
        date=date(2026, 7, 25),
        amount=Decimal("1"),
        type=TransactionType.EXPENSE,
        category="A",
    )
    earlier = repo.create(
        date=date(2026, 7, 20),
        amount=Decimal("1"),
        type=TransactionType.EXPENSE,
        category="B",
    )

    transactions = repo.list()

    assert [t.id for t in transactions] == [earlier.id, later.id]


def test_update_changes_fields(repo):
    created = repo.create(
        date=date(2026, 7, 24),
        amount=Decimal("10"),
        type=TransactionType.EXPENSE,
        category="Old",
    )

    updated = repo.update(created.id, amount=Decimal("20"), category="New")

    assert updated is not None
    assert updated.amount == Decimal("20")
    assert updated.category == "New"


def test_update_returns_none_for_unknown_id(repo):
    assert repo.update(999, category="Whatever") is None


def test_delete_removes_transaction(repo):
    created = repo.create(
        date=date(2026, 7, 24),
        amount=Decimal("10"),
        type=TransactionType.EXPENSE,
        category="To delete",
    )

    assert repo.delete(created.id) is True
    assert repo.get(created.id) is None


def test_delete_returns_false_for_unknown_id(repo):
    assert repo.delete(999) is False
