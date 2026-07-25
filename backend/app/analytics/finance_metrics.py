from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.analytics.views import daily_finance_metrics
from app.models.transaction import Transaction, TransactionType


def get_daily_finance_metrics(session: Session, category: str | None = None):
    stmt = select(daily_finance_metrics)
    if category is not None:
        stmt = stmt.where(daily_finance_metrics.c.category == category)
    stmt = stmt.order_by(daily_finance_metrics.c.day, daily_finance_metrics.c.category)
    return session.execute(stmt).all()


def get_balance(session: Session) -> Decimal:
    income_total = session.scalar(
        select(func.coalesce(func.sum(Transaction.amount), 0)).where(
            Transaction.type == TransactionType.INCOME
        )
    )
    expense_total = session.scalar(
        select(func.coalesce(func.sum(Transaction.amount), 0)).where(
            Transaction.type == TransactionType.EXPENSE
        )
    )
    return income_total - expense_total
