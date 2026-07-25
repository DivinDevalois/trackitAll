from datetime import date, datetime, timedelta, timezone

from app.analytics.correlation import get_habit_task_correlation
from app.models.habit import Habit
from app.models.habit_log import HabitLog
from app.models.task import Task, TaskStatus


def _utc(d: date) -> datetime:
    return datetime(d.year, d.month, d.day, tzinfo=timezone.utc)


def _add_completed_tasks(db_session, day: date, count: int) -> None:
    for _ in range(count):
        db_session.add(
            Task(title="t", status=TaskStatus.DONE, created_at=_utc(day), completed_at=_utc(day))
        )


def test_computes_daily_rate_and_good_vs_bad_summary(db_session):
    today = date.today()
    d3, d2, d1, d0 = (today - timedelta(days=n) for n in (3, 2, 1, 0))

    habit = Habit(name="Gym", created_at=_utc(d3))
    db_session.add(habit)
    db_session.flush()

    db_session.add_all(
        [
            HabitLog(habit_id=habit.id, date=d3, completed=True),
            HabitLog(habit_id=habit.id, date=d2, completed=True),
        ]
    )
    _add_completed_tasks(db_session, d3, 5)
    _add_completed_tasks(db_session, d2, 3)
    _add_completed_tasks(db_session, d1, 1)
    # d0: no completed tasks at all
    db_session.commit()

    days = get_habit_task_correlation(db_session, window_days=4)

    by_day = {row["day"]: row for row in days}
    assert by_day[d3] == {"day": d3, "tasks_completed": 5, "habit_completion_rate": 1.0}
    assert by_day[d2] == {"day": d2, "tasks_completed": 3, "habit_completion_rate": 1.0}
    assert by_day[d1] == {"day": d1, "tasks_completed": 1, "habit_completion_rate": 0.0}
    assert by_day[d0] == {"day": d0, "tasks_completed": 0, "habit_completion_rate": 0.0}


def test_excludes_habit_before_its_creation_date(db_session):
    today = date.today()
    d1, d0 = (today - timedelta(days=n) for n in (1, 0))

    habit = Habit(name="Gym", created_at=_utc(d0))
    db_session.add(habit)
    db_session.flush()
    db_session.add(HabitLog(habit_id=habit.id, date=d0, completed=True))
    db_session.commit()

    days = get_habit_task_correlation(db_session, window_days=2)

    by_day = {row["day"]: row for row in days}
    assert by_day[d1]["habit_completion_rate"] is None
    assert by_day[d0]["habit_completion_rate"] == 1.0


def test_excludes_paused_habits(db_session):
    today = date.today()
    d1, d0 = (today - timedelta(days=n) for n in (1, 0))

    active = Habit(name="Active", created_at=_utc(d1), is_active=True)
    paused = Habit(name="Paused", created_at=_utc(d1), is_active=False)
    db_session.add_all([active, paused])
    db_session.flush()
    # The paused habit was never checked in — if it still counted, both
    # days would show a 0% rate instead of 100%.
    db_session.add_all(
        [
            HabitLog(habit_id=active.id, date=d1, completed=True),
            HabitLog(habit_id=active.id, date=d0, completed=True),
        ]
    )
    db_session.commit()

    days = get_habit_task_correlation(db_session, window_days=2)

    by_day = {row["day"]: row for row in days}
    assert by_day[d1]["habit_completion_rate"] == 1.0
    assert by_day[d0]["habit_completion_rate"] == 1.0
