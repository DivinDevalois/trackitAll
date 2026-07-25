from datetime import date, timedelta

from app.analytics.streaks import get_habit_streaks
from app.repositories.habit_log_repository import HabitLogRepository
from app.repositories.habit_repository import HabitRepository


def test_no_logs_gives_zero_streaks(db_session):
    HabitRepository(db_session).create(name="Gym")

    streaks = get_habit_streaks(db_session)

    assert streaks == [
        {"habit_id": streaks[0]["habit_id"], "habit_name": "Gym", "current_streak": 0, "longest_streak": 0}
    ]


def test_longest_streak_survives_a_gap_even_if_current_streak_is_shorter(db_session):
    habit = HabitRepository(db_session).create(name="Gym")
    log_repo = HabitLogRepository(db_session)
    today = date.today()

    # An earlier 5-day run, then a gap, then a shorter 3-day run ending today.
    for offset in range(9, 4, -1):  # d-9..d-5: 5 consecutive days
        log_repo.check_in(habit.id, today - timedelta(days=offset))
    # d-4 is a gap (no check-in)
    for offset in range(2, -1, -1):  # d-2..d0: 3 consecutive days
        log_repo.check_in(habit.id, today - timedelta(days=offset))

    streaks = get_habit_streaks(db_session)

    assert streaks[0]["current_streak"] == 3
    assert streaks[0]["longest_streak"] == 5


def test_current_streak_is_not_broken_by_today_not_being_logged_yet(db_session):
    habit = HabitRepository(db_session).create(name="Gym")
    log_repo = HabitLogRepository(db_session)
    today = date.today()

    for offset in range(2, 0, -1):  # d-2, d-1 completed; today not logged
        log_repo.check_in(habit.id, today - timedelta(days=offset))

    streaks = get_habit_streaks(db_session)

    assert streaks[0]["current_streak"] == 2


def test_current_streak_is_zero_if_yesterday_was_missed(db_session):
    habit = HabitRepository(db_session).create(name="Gym")
    log_repo = HabitLogRepository(db_session)
    today = date.today()

    log_repo.check_in(habit.id, today - timedelta(days=5))

    streaks = get_habit_streaks(db_session)

    assert streaks[0]["current_streak"] == 0
    assert streaks[0]["longest_streak"] == 1


def test_incomplete_check_in_does_not_count_toward_streak(db_session):
    habit = HabitRepository(db_session).create(name="Gym")
    log_repo = HabitLogRepository(db_session)
    today = date.today()

    log_repo.check_in(habit.id, today, completed=False)

    streaks = get_habit_streaks(db_session)

    assert streaks[0]["current_streak"] == 0
    assert streaks[0]["longest_streak"] == 0
