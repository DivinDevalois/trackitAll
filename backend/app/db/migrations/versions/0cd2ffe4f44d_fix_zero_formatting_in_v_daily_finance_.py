"""fix zero formatting in v_daily_finance_metrics

Revision ID: 0cd2ffe4f44d
Revises: bf770c3601f2
Create Date: 2026-07-24 18:18:21.494331

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0cd2ffe4f44d'
down_revision: Union[str, Sequence[str], None] = 'bf770c3601f2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # The literal 0 fallback in COALESCE doesn't carry the numeric(12,2)
    # scale that SUM(amount) does, so it rendered as "0" instead of "0.00".
    op.execute(
        """
        CREATE OR REPLACE VIEW v_daily_finance_metrics AS
        SELECT
            date AS day,
            category,
            COALESCE(SUM(amount) FILTER (WHERE type = 'income'), 0::numeric(12, 2)) AS income,
            COALESCE(SUM(amount) FILTER (WHERE type = 'expense'), 0::numeric(12, 2)) AS expense
        FROM transaction
        GROUP BY date, category
        ORDER BY date, category
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        """
        CREATE OR REPLACE VIEW v_daily_finance_metrics AS
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
