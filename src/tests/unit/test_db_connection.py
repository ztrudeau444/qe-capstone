"""Unit tests for db(), TalkDesk's database connection helper.

These check the safety check added when the hard-coded database password was
removed (SonarQube blocker, 2026-10-09): if the DB_URL setting is missing,
db() must stop with a clear error and log it, instead of trying to connect
with no address.
"""
import logging

import pytest

import talkdesk.app as app_module
from talkdesk.app import db

# Log messages from this test file appear under its own name, so in a test
# report it's easy to see which test said what.
logger = logging.getLogger(__name__)


def test_db_stops_with_a_clear_error_when_db_url_is_missing(monkeypatch, caplog):
    """db() refuses to connect, and logs why, when DB_URL is not set.

    Steps:
      1. Arrange: pretend the DB_URL setting is missing. monkeypatch changes
         it for this one test only and puts it back afterwards, so no other
         test is affected.
      2. Arrange: start recording TalkDesk's error messages. caplog is
         pytest's tool for capturing log messages so a test can check them.
      3. Act and assert: call db() and expect it to stop with a RuntimeError
         whose message names DB_URL, so whoever reads it knows what to fix.
      4. Assert: check that TalkDesk also logged the problem, so it would be
         visible in the app's output, not only in the error.
    """
    # Step 1: remove the database address for this test only.
    logger.info("Arrange: removing DB_URL for this test only")
    monkeypatch.setattr(app_module, "DB_URL", None)

    # Step 2: record anything TalkDesk logs at ERROR level.
    caplog.set_level(logging.ERROR, logger="talkdesk")

    # Step 3: db() must refuse, with a message that names the missing setting.
    logger.info("Act: calling db() with no DB_URL")
    with pytest.raises(RuntimeError, match="DB_URL is not set"):
        db()

    # Step 4: the problem must also appear in TalkDesk's log.
    logger.info("Assert: checking that TalkDesk logged the problem")
    assert "DB_URL is not set" in caplog.text