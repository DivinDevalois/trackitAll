from datetime import date

from sqlalchemy import text

from app.repositories.habit_log_repository import HabitLogRepository
from app.repositories.habit_repository import HabitRepository


def test_v_daily_habit_metrics_returns_daily_facts_per_habit(db_session):
    habit_repo = HabitRepository(db_session)
    log_repo = HabitLogRepository(db_session)

    gym = habit_repo.create(name="Gym")
    reading = habit_repo.create(name="Read")

    log_repo.check_in(gym.id, date(2026, 7, 20), completed=True)
    log_repo.check_in(gym.id, date(2026, 7, 21), completed=False)
    log_repo.check_in(gym.id, date(2026, 7, 22), completed=True)
    log_repo.check_in(reading.id, date(2026, 7, 20), completed=True)

    rows = db_session.execute(
        text("SELECT habit_id, habit_name, day, completed FROM v_daily_habit_metrics")
    ).all()

    assert [tuple(row) for row in rows] == [
        (gym.id, "Gym", date(2026, 7, 20), True),
        (gym.id, "Gym", date(2026, 7, 21), False),
        (gym.id, "Gym", date(2026, 7, 22), True),
        (reading.id, "Read", date(2026, 7, 20), True),
    ]


def test_v_daily_habit_metrics_can_compute_a_consistency_rate(db_session):
    habit_repo = HabitRepository(db_session)
    log_repo = HabitLogRepository(db_session)

    gym = habit_repo.create(name="Gym")
    log_repo.check_in(gym.id, date(2026, 7, 20), completed=True)
    log_repo.check_in(gym.id, date(2026, 7, 21), completed=False)
    log_repo.check_in(gym.id, date(2026, 7, 22), completed=True)
    log_repo.check_in(gym.id, date(2026, 7, 23), completed=True)

    rate = db_session.execute(
        text(
            """
            SELECT AVG(completed::int)
            FROM v_daily_habit_metrics
            WHERE habit_id = :habit_id AND day BETWEEN :start AND :end
            """
        ),
        {"habit_id": gym.id, "start": date(2026, 7, 20), "end": date(2026, 7, 23)},
    ).scalar_one()

    assert float(rate) == 0.75
