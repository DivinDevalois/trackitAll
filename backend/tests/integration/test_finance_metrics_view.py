from datetime import date
from decimal import Decimal

from sqlalchemy import text

from app.models.transaction import Transaction, TransactionType


def test_v_daily_finance_metrics_aggregates_by_day_and_category(db_session):
    db_session.add_all(
        [
            Transaction(
                date=date(2026, 7, 20),
                amount=Decimal("2000"),
                type=TransactionType.INCOME,
                category="Salaire",
            ),
            Transaction(
                date=date(2026, 7, 20),
                amount=Decimal("30.50"),
                type=TransactionType.EXPENSE,
                category="Alimentation",
            ),
            Transaction(
                date=date(2026, 7, 20),
                amount=Decimal("15"),
                type=TransactionType.EXPENSE,
                category="Alimentation",
            ),
            Transaction(
                date=date(2026, 7, 21),
                amount=Decimal("50"),
                type=TransactionType.EXPENSE,
                category="Transport",
            ),
        ]
    )
    db_session.commit()

    rows = db_session.execute(
        text("SELECT day, category, income, expense FROM v_daily_finance_metrics")
    ).all()

    assert [tuple(row) for row in rows] == [
        (date(2026, 7, 20), "Alimentation", Decimal("0"), Decimal("45.50")),
        (date(2026, 7, 20), "Salaire", Decimal("2000.00"), Decimal("0")),
        (date(2026, 7, 21), "Transport", Decimal("0"), Decimal("50.00")),
    ]
