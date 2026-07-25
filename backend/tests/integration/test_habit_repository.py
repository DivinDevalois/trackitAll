from datetime import time

import pytest

from app.models.habit import HabitType
from app.repositories.habit_repository import HabitRepository


@pytest.fixture()
def repo(db_session):
    return HabitRepository(db_session)


def test_create_sets_defaults(repo):
    habit = repo.create(name="Read 20 minutes")

    assert habit.id is not None
    assert habit.name == "Read 20 minutes"
    assert habit.target_frequency_per_week == 7
    assert habit.type == HabitType.BUILD
    assert habit.description is None
    assert habit.target_time is None
    assert habit.is_active is True


def test_create_accepts_break_type_description_and_target_time(repo):
    habit = repo.create(
        name="Ne pas procrastiner",
        description="Éviter de remettre les tâches importantes au lendemain",
        type=HabitType.BREAK,
        target_time=time(9, 0),
    )

    assert habit.type == HabitType.BREAK
    assert habit.description == "Éviter de remettre les tâches importantes au lendemain"
    assert habit.target_time == time(9, 0)


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


def test_update_changes_enriched_fields(repo):
    created = repo.create(name="Gym", type=HabitType.BUILD)

    updated = repo.update(
        created.id,
        description="Updated description",
        type=HabitType.BREAK,
        target_time=time(18, 30),
    )

    assert updated is not None
    assert updated.description == "Updated description"
    assert updated.type == HabitType.BREAK
    assert updated.target_time == time(18, 30)


def test_delete_removes_habit(repo):
    created = repo.create(name="To delete")

    assert repo.delete(created.id) is True
    assert repo.get(created.id) is None


def test_delete_returns_false_for_unknown_id(repo):
    assert repo.delete(999) is False


def test_update_toggles_is_active(repo):
    created = repo.create(name="Gym")

    paused = repo.update(created.id, is_active=False)
    assert paused.is_active is False

    resumed = repo.update(created.id, is_active=True)
    assert resumed.is_active is True


def test_list_active_only_excludes_paused_habits(repo):
    active = repo.create(name="Active habit")
    paused = repo.create(name="Paused habit")
    repo.update(paused.id, is_active=False)

    habits = repo.list(active_only=True)

    assert [h.id for h in habits] == [active.id]
