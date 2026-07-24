from sqlalchemy import select
from sqlalchemy.orm import Session

from app.analytics.views import daily_habit_metrics


def get_daily_habit_metrics(session: Session, habit_id: int | None = None):
    stmt = select(daily_habit_metrics)
    if habit_id is not None:
        stmt = stmt.where(daily_habit_metrics.c.habit_id == habit_id)
    stmt = stmt.order_by(daily_habit_metrics.c.habit_id, daily_habit_metrics.c.day)
    return session.execute(stmt).all()
