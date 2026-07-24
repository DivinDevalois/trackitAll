from pathlib import Path

import psycopg
import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.db.config import POSTGRES_TEST_DB, database_url

BACKEND_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def db_engine():
    """SQLAlchemy engine on a dedicated test database, migrated to head."""
    with psycopg.connect(database_url("postgres", driver=""), autocommit=True) as conn:
        exists = conn.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s", (POSTGRES_TEST_DB,)
        ).fetchone()
        if not exists:
            conn.execute(f'CREATE DATABASE "{POSTGRES_TEST_DB}"')

    test_db_url = database_url(POSTGRES_TEST_DB)

    alembic_cfg = Config(str(BACKEND_ROOT / "alembic.ini"))
    alembic_cfg.set_main_option("sqlalchemy.url", test_db_url)
    command.upgrade(alembic_cfg, "head")

    engine = create_engine(test_db_url)
    yield engine
    engine.dispose()


@pytest.fixture()
def db_session(db_engine):
    """Session on the test database, with tables truncated after each test."""
    session_factory = sessionmaker(bind=db_engine, expire_on_commit=False)
    session = session_factory()
    try:
        yield session
    finally:
        session.close()
        with db_engine.begin() as conn:
            conn.execute(text("TRUNCATE TABLE task RESTART IDENTITY CASCADE"))
