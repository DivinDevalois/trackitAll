"""create v_daily_finance_metrics view

Revision ID: bf770c3601f2
Revises: 6358e16f852d
Create Date: 2026-07-24 18:13:32.845827

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bf770c3601f2'
down_revision: Union[str, Sequence[str], None] = '6358e16f852d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
        CREATE VIEW v_daily_finance_metrics AS
        SELECT
            date AS day,
            category,
            COALESCE(SUM(amount) FILTER (WHERE type = 'income'), 0) AS income,
            COALESCE(SUM(amount) FILTER (WHERE type = 'expense'), 0) AS expense
        FROM transaction
        GROUP BY date, category
        ORDER BY date, category
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP VIEW v_daily_finance_metrics")
