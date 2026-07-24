from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.analytics.habit_metrics import get_daily_habit_metrics
from app.analytics.task_metrics import get_daily_task_metrics
from app.repositories.habit_repository import HabitRepository


def get_habit_task_correlation(session: Session, *, window_days: int = 30) -> list[dict]:
    """Daily task velocity next to daily habit completion rate, over a trailing window.

    habit_completion_rate for a given day is the fraction of habits that
    already existed by that day which were checked in as completed — habits
    created after a given day don't count against it, and a day with no
    log at all for a habit counts as not completed (see v_daily_habit_metrics,
    which only records logged days).
    """
    end = date.today()
    start = end - timedelta(days=window_days - 1)
    days = [start + timedelta(days=offset) for offset in range(window_days)]

    tasks_completed_by_day = {row.day: row.tasks_completed for row in get_daily_task_metrics(session)}
    completed_by_habit_day = {
        (row.habit_id, row.day): row.completed for row in get_daily_habit_metrics(session)
    }
    habits = HabitRepository(session).list()

    results = []
    for day in days:
        active_habits = [h for h in habits if h.created_at.date() <= day]
        if active_habits:
            completed_count = sum(
                1 for h in active_habits if completed_by_habit_day.get((h.id, day), False)
            )
            habit_completion_rate = completed_count / len(active_habits)
        else:
            habit_completion_rate = None
        results.append(
            {
                "day": day,
                "tasks_completed": tasks_completed_by_day.get(day, 0),
                "habit_completion_rate": habit_completion_rate,
            }
        )
    return results
