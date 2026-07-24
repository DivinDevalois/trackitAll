import os
from pathlib import Path

from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[3]
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


def database_url(dbname: str, driver: str = "+psycopg") -> str:
    return f"postgresql{driver}://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:{POSTGRES_PORT}/{dbname}"
