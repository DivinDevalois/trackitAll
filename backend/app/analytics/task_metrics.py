from sqlalchemy import select
from sqlalchemy.orm import Session

from app.analytics.views import daily_task_metrics


def get_daily_task_metrics(session: Session):
    stmt = select(daily_task_metrics).order_by(daily_task_metrics.c.day)
    return session.execute(stmt).all()
