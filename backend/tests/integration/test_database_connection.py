from sqlalchemy import text

from tests.conftest import POSTGRES_DB, POSTGRES_TEST_DB


def test_connects_to_an_isolated_test_database(db_engine):
    assert db_engine.url.database == POSTGRES_TEST_DB
    assert db_engine.url.database != POSTGRES_DB

    with db_engine.connect() as conn:
        result = conn.execute(text("SELECT 1")).scalar_one()

    assert result == 1
