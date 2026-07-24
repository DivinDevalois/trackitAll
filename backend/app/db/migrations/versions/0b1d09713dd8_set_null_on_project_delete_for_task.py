"""set null on project delete for task

Revision ID: 0b1d09713dd8
Revises: a11c05f5e076
Create Date: 2026-07-24 16:51:49.577808

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0b1d09713dd8'
down_revision: Union[str, Sequence[str], None] = 'a11c05f5e076'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint("fk_task_project_id_project", "task", type_="foreignkey")
    op.create_foreign_key(
        "fk_task_project_id_project",
        "task",
        "project",
        ["project_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("fk_task_project_id_project", "task", type_="foreignkey")
    op.create_foreign_key(
        "fk_task_project_id_project", "task", "project", ["project_id"], ["id"]
    )
