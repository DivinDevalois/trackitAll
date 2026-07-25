from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.repositories.habit_log_repository import HabitLogRepository
from app.repositories.habit_repository import HabitRepository


def get_habit_streaks(session: Session) -> list[dict]:
    """Current and longest run of consecutive completed days, per habit."""
    habits = HabitRepository(session).list()
    log_repo = HabitLogRepository(session)

    results = []
    for habit in habits:
        completed_dates = sorted(
            log.date for log in log_repo.list_for_habit(habit.id) if log.completed
        )

        longest_streak = 0
        running_streak = 0
        previous_date: date | None = None
        for day in completed_dates:
            if previous_date is not None and day == previous_date + timedelta(days=1):
                running_streak += 1
            else:
                running_streak = 1
            longest_streak = max(longest_streak, running_streak)
            previous_date = day

        completed_set = set(completed_dates)
        # A streak isn't broken just because today hasn't been checked in
        # yet — only anchor on today if it's already logged, otherwise
        # start counting backwards from yesterday.
        cursor = date.today()
        if cursor not in completed_set:
            cursor -= timedelta(days=1)
        current_streak = 0
        while cursor in completed_set:
            current_streak += 1
            cursor -= timedelta(days=1)

        results.append(
            {
                "habit_id": habit.id,
                "habit_name": habit.name,
                "current_streak": current_streak,
                "longest_streak": longest_streak,
            }
        )
    return results
