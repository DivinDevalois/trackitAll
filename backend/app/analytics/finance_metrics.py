from sqlalchemy import select
from sqlalchemy.orm import Session

from app.analytics.views import daily_finance_metrics


def get_daily_finance_metrics(session: Session, category: str | None = None):
    stmt = select(daily_finance_metrics)
    if category is not None:
        stmt = stmt.where(daily_finance_metrics.c.category == category)
    stmt = stmt.order_by(daily_finance_metrics.c.day, daily_finance_metrics.c.category)
    return session.execute(stmt).all()
