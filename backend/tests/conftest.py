import os
from pathlib import Path

import psycopg
import pytest
from alembic import command
from alembic.config import Config
from dotenv import load_dotenv
from sqlalchemy import create_engine

BACKEND_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = BACKEND_ROOT.parent

load_dotenv(REPO_ROOT / ".env")

POSTGRES_USER = os.environ["POSTGRES_USER"]
POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", "5432")
POSTGRES_DB = os.environ["POSTGRES_DB"]
POSTGRES_TEST_DB = os.environ.get("POSTGRES_TEST_DB", "trackitall_test")

if POSTGRES_TEST_DB == POSTGRES_DB:
    raise RuntimeError(
        "POSTGRES_TEST_DB must differ from POSTGRES_DB, otherwise tests would run "
        "against (and wipe) the dev database."
    )


def _connection_string(dbname: str, driver: str = "") -> str:
    return f"postgresql{driver}://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:{POSTGRES_PORT}/{dbname}"


@pytest.fixture(scope="session")
def db_engine():
    """SQLAlchemy engine on a dedicated test database, migrated to head."""
    with psycopg.connect(_connection_string("postgres"), autocommit=True) as conn:
        exists = conn.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s", (POSTGRES_TEST_DB,)
        ).fetchone()
        if not exists:
            conn.execute(f'CREATE DATABASE "{POSTGRES_TEST_DB}"')

    test_db_url = _connection_string(POSTGRES_TEST_DB, driver="+psycopg")

    alembic_cfg = Config(str(BACKEND_ROOT / "alembic.ini"))
    alembic_cfg.set_main_option("sqlalchemy.url", test_db_url)
    command.upgrade(alembic_cfg, "head")

    engine = create_engine(test_db_url)
    yield engine
    engine.dispose()
