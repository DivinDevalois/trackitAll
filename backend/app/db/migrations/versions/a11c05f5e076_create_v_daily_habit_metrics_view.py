"""create v_daily_habit_metrics view

Revision ID: a11c05f5e076
Revises: 534f66a9b749
Create Date: 2026-07-24 14:49:23.420076

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a11c05f5e076'
down_revision: Union[str, Sequence[str], None] = '534f66a9b749'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
        CREATE VIEW v_daily_habit_metrics AS
        SELECT
            h.id AS habit_id,
            h.name AS habit_name,
            hl.date AS day,
            hl.completed
        FROM habit h
        JOIN habit_log hl ON hl.habit_id = h.id
        ORDER BY h.id, hl.date
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP VIEW v_daily_habit_metrics")
