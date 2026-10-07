"""Shared setup for unit tests."""
import pytest

import talkdesk.app as app_module


@pytest.fixture
def no_database(monkeypatch):
    """Replace the database with a stand-in that fails if it is ever used.
    A unit test that asks for this proves the code decided without the database."""
    def database_must_not_be_touched():
        raise AssertionError("the database must not be touched")

    monkeypatch.setattr(app_module, "db", database_must_not_be_touched)
