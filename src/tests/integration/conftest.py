"""Shared setup for integration tests: the real TalkDesk API against a real database."""
import os
from pathlib import Path

import psycopg
import pytest
from fastapi.testclient import TestClient

import talkdesk.app as app_module

# The pipeline sets DB_URL; on a laptop it points at the docker compose database.
DB_URL = os.environ.get("DB_URL", "postgresql://qe:qe@127.0.0.1:5432/qe")
DB_DIR = Path(__file__).resolve().parents[3] / "db"


@pytest.fixture(scope="session")
def database():
    """A database with TalkDesk's schema and seed data.
    docker compose loads these on start; the pipeline's database starts empty,
    so they are loaded here when the tables are missing."""
    with psycopg.connect(DB_URL, autocommit=True) as conn:
        if conn.execute("SELECT to_regclass('public.talks')").fetchone()[0] is None:
            for script in ("01-schema.sql", "02-seed.sql"):
                conn.execute((DB_DIR / script).read_text(encoding="utf-8"))
    return DB_URL


@pytest.fixture
def client(database, monkeypatch):
    """Calls TalkDesk's real API, which talks to the real database."""
    monkeypatch.setattr(app_module, "DB_URL", database)
    with TestClient(app_module.app) as c:
        yield c


@pytest.fixture
def talk_count(database):
    """Counts talks straight from the database, to prove what did or did not change."""
    def count():
        with psycopg.connect(database) as conn:
            return conn.execute("SELECT count(*) FROM talks").fetchone()[0]
    return count


# TEMPORARY: proving the coverage gate bites (Week 2 workbook 4b).
# Skips every integration test; undone by the next commit.
collect_ignore_glob = ["test_*.py"]
