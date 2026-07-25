from datetime import date

import pytest

from app.repositories.habit_log_repository import HabitLogRepository
from app.repositories.habit_repository import HabitRepository


@pytest.fixture()
def habit_repo(db_session):
    return HabitRepository(db_session)


@pytest.fixture()
def log_repo(db_session):
    return HabitLogRepository(db_session)


@pytest.fixture()
def habit(habit_repo):
    return habit_repo.create(name="Read 20 minutes")


def test_check_in_creates_a_log(log_repo, habit):
    log = log_repo.check_in(habit.id, date(2026, 7, 24))

    assert log.habit_id == habit.id
    assert log.date == date(2026, 7, 24)
    assert log.completed is True


def test_check_in_twice_same_day_does_not_duplicate(log_repo, habit):
    first = log_repo.check_in(habit.id, date(2026, 7, 24))
    second = log_repo.check_in(habit.id, date(2026, 7, 24))

    assert first.id == second.id
    assert len(log_repo.list_for_habit(habit.id)) == 1


def test_check_in_twice_same_day_updates_completed(log_repo, habit):
    log_repo.check_in(habit.id, date(2026, 7, 24), completed=True)
    updated = log_repo.check_in(habit.id, date(2026, 7, 24), completed=False)

    assert updated.completed is False


def test_list_for_habit_returns_logs_ordered_by_date(log_repo, habit):
    log_repo.check_in(habit.id, date(2026, 7, 24))
    log_repo.check_in(habit.id, date(2026, 7, 22))

    logs = log_repo.list_for_habit(habit.id)

    assert [log.date for log in logs] == [date(2026, 7, 22), date(2026, 7, 24)]


def test_list_for_habit_does_not_include_other_habits(log_repo, habit_repo, habit):
    other_habit = habit_repo.create(name="Gym")
    log_repo.check_in(other_habit.id, date(2026, 7, 24))

    assert log_repo.list_for_habit(habit.id) == []


def test_check_in_accepts_duration_minutes(log_repo, habit):
    log = log_repo.check_in(habit.id, date(2026, 7, 24), duration_minutes=20)

    assert log.duration_minutes == 20


def test_check_in_twice_same_day_updates_duration(log_repo, habit):
    log_repo.check_in(habit.id, date(2026, 7, 24), duration_minutes=20)
    updated = log_repo.check_in(habit.id, date(2026, 7, 24), duration_minutes=35)

    assert updated.duration_minutes == 35
