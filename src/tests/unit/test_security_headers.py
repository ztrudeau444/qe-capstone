"""Unit test: every TalkDesk reply carries the security headers.

Added after the first ZAP baseline scan (2026-10-13) reported them missing:
rules 10020, 10021, 10038, 10063 (FAIL in quality/security/zap-rules.tsv)
and 10049, 90004 (WARN).

The test asks for a page that does not exist. TalkDesk answers 404 without
touching the database, and even that reply must carry the headers: an
attacker does not only visit the pages that work.
"""
import logging

import pytest
from fastapi.testclient import TestClient

from talkdesk.app import SECURITY_HEADERS, app

logger = logging.getLogger(__name__)


@pytest.mark.unit
def test_every_reply_carries_the_security_headers():
    """A 404 reply carries every header in SECURITY_HEADERS, with its value.

    Steps:
      1. Arrange: a test client that calls TalkDesk directly, no server needed.
      2. Act: request a page that does not exist.
      3. Assert: the reply is a 404, and each security header is present
         with exactly the expected value.
    """
    # Step 1: a client that talks to the app in memory.
    client = TestClient(app)

    # Step 2: a page that does not exist.
    logger.info("Act: requesting a page that does not exist")
    reply = client.get("/no-such-page")

    # Step 3: right status, and every header present with the right value.
    assert reply.status_code == 404
    for name, value in SECURITY_HEADERS.items():
        logger.info("Assert: %s is %r", name, value)
        assert reply.headers.get(name) == value, f"{name} is missing or wrong"