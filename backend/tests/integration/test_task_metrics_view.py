from datetime import date, datetime, timezone

from sqlalchemy import text

from app.models.task import Task, TaskStatus


def _utc(year: int, month: int, day: int, hour: int = 0) -> datetime:
    return datetime(year, month, day, hour, tzinfo=timezone.utc)


def test_v_daily_task_metrics_aggregates_created_and_completed_by_day(db_session):
    tasks = [
        Task(
            title="A",
            status=TaskStatus.DONE,
            created_at=_utc(2026, 7, 19),
            completed_at=_utc(2026, 7, 22),
        ),
        Task(title="B", status=TaskStatus.TODO, created_at=_utc(2026, 7, 20)),
        Task(
            title="C",
            status=TaskStatus.DONE,
            created_at=_utc(2026, 7, 20),
            completed_at=_utc(2026, 7, 21),
        ),
        Task(
            title="D",
            status=TaskStatus.DONE,
            created_at=_utc(2026, 7, 21),
            completed_at=_utc(2026, 7, 21),
        ),
    ]
    db_session.add_all(tasks)
    db_session.commit()

    rows = db_session.execute(
        text("SELECT day, tasks_created, tasks_completed FROM v_daily_task_metrics ORDER BY day")
    ).all()

    assert [tuple(row) for row in rows] == [
        (date(2026, 7, 19), 1, 0),
        (date(2026, 7, 20), 2, 0),
        (date(2026, 7, 21), 1, 2),
        (date(2026, 7, 22), 0, 1),
    ]


def test_v_daily_task_metrics_ignores_updates_unrelated_to_completion(db_session):
    task = Task(
        title="A",
        status=TaskStatus.DONE,
        created_at=_utc(2026, 7, 19),
        completed_at=_utc(2026, 7, 19),
    )
    db_session.add(task)
    db_session.commit()

    task.title = "A (renamed later)"
    db_session.commit()

    rows = db_session.execute(
        text("SELECT tasks_completed FROM v_daily_task_metrics WHERE day = :day"),
        {"day": date(2026, 7, 19)},
    ).all()

    assert rows == [(1,)]
