from sqlalchemy import Boolean, Column, Date, Integer, MetaData, String, Table

# Separate from app.db.base.Base.metadata on purpose: these Table objects
# describe read-only SQL views (created by hand-written migrations, see
# app/db/migrations/versions/534f66a9b749_* and a11c05f5e076_*), not tables
# Alembic should manage. Alembic's autogenerate only diffs Base.metadata
# against the DB's tables (not views) — attaching these there would make it
# think the views are missing tables and try to (re)create them.
metadata = MetaData()

daily_task_metrics = Table(
    "v_daily_task_metrics",
    metadata,
    Column("day", Date, primary_key=True),
    Column("tasks_created", Integer),
    Column("tasks_completed", Integer),
)

daily_habit_metrics = Table(
    "v_daily_habit_metrics",
    metadata,
    Column("habit_id", Integer),
    Column("habit_name", String),
    Column("day", Date),
    Column("completed", Boolean),
)
