"""Shared test setup: the base layer.

Two fixtures every integration test can ask for by name:
    database  a database holding TalkDesk's schema and seed data
    api       TalkDesk's real API, talking to that database

src/tests/conftest.py imports them, which makes them available to every test.
"""
from pathlib import Path

import psycopg
import pytest
from fastapi.testclient import TestClient

import talkdesk.app as app_module
from config import settings
from pages.talkdesk_api import TalkDeskApi

DB_DIR = Path(__file__).resolve().parents[2] / "db"


@pytest.fixture(scope="session")
def database():
    """docker compose loads the schema and seed on start; the pipeline's
    database starts empty, so they are loaded here when the tables are missing."""
    with psycopg.connect(settings.DB_URL, autocommit=True) as conn:
        if conn.execute("SELECT to_regclass('public.talks')").fetchone()[0] is None:
            for script in ("01-schema.sql", "02-seed.sql"):
                conn.execute((DB_DIR / script).read_text(encoding="utf-8"))
    return settings.DB_URL


@pytest.fixture
def api(database, monkeypatch):
    monkeypatch.setattr(app_module, "DB_URL", database)
    with TestClient(app_module.app) as client:
        yield TalkDeskApi(client)
