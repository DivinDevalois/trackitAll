"""create v_daily_task_metrics view

Revision ID: 534f66a9b749
Revises: 235ba4f34fe4
Create Date: 2026-07-24 13:17:04.573712

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '534f66a9b749'
down_revision: Union[str, Sequence[str], None] = '235ba4f34fe4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
        CREATE VIEW v_daily_task_metrics AS
        WITH created AS (
            SELECT date_trunc('day', created_at)::date AS day, COUNT(*) AS tasks_created
            FROM task
            GROUP BY 1
        ),
        completed AS (
            SELECT date_trunc('day', completed_at)::date AS day, COUNT(*) AS tasks_completed
            FROM task
            WHERE completed_at IS NOT NULL
            GROUP BY 1
        )
        SELECT
            COALESCE(created.day, completed.day) AS day,
            COALESCE(created.tasks_created, 0) AS tasks_created,
            COALESCE(completed.tasks_completed, 0) AS tasks_completed
        FROM created
        FULL OUTER JOIN completed ON created.day = completed.day
        ORDER BY day
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP VIEW v_daily_task_metrics")
