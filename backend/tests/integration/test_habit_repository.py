import pytest

from app.repositories.habit_repository import HabitRepository


@pytest.fixture()
def repo(db_session):
    return HabitRepository(db_session)


def test_create_sets_default_frequency(repo):
    habit = repo.create(name="Read 20 minutes")

    assert habit.id is not None
    assert habit.name == "Read 20 minutes"
    assert habit.target_frequency_per_week == 7


def test_create_accepts_explicit_frequency(repo):
    habit = repo.create(name="Gym", target_frequency_per_week=3)

    assert habit.target_frequency_per_week == 3


def test_get_returns_none_for_unknown_id(repo):
    assert repo.get(999) is None


def test_list_returns_all_habits_ordered_by_id(repo):
    first = repo.create(name="First")
    second = repo.create(name="Second")

    habits = repo.list()

    assert [h.id for h in habits] == [first.id, second.id]


def test_update_changes_fields(repo):
    created = repo.create(name="Old name", target_frequency_per_week=7)

    updated = repo.update(created.id, name="New name", target_frequency_per_week=5)

    assert updated is not None
    assert updated.name == "New name"
    assert updated.target_frequency_per_week == 5


def test_update_returns_none_for_unknown_id(repo):
    assert repo.update(999, name="Whatever") is None


def test_delete_removes_habit(repo):
    created = repo.create(name="To delete")

    assert repo.delete(created.id) is True
    assert repo.get(created.id) is None


def test_delete_returns_false_for_unknown_id(repo):
    assert repo.delete(999) is False
