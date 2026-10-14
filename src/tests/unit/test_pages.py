"""Unit tests: TalkDesk's web pages render real HTML, not "Handler.".

The shared page template (PAGE in app.py) was a planted defect: it held only
the word "Handler.", with no {title} or {body} placeholders, so every page
showed that word and nothing else (gap list #3, confirmed planted by the
instructor 2026-10-09). This blocked AC-13 (sign-in page accessible) and
AC-14 (browse to a talk).

The sign-in page is tested here because it needs no database. The home page
needs the database and is covered by the E2E test for AC-14.
"""
import logging

import pytest
from fastapi.testclient import TestClient

from talkdesk.app import app

logger = logging.getLogger(__name__)


@pytest.mark.unit
def test_sign_in_page_renders_the_form():
    """The sign-in page is a real, labelled HTML form inside the template.

    Steps:
      1. Arrange: a test client that calls TalkDesk directly.
      2. Act: open the sign-in page.
      3. Assert: it is not "Handler."; it has the page language and its
         own title (both needed for accessibility, AC-13); and it contains
         the form with a label for each field.
    """
    # Step 1: a client that talks to the app in memory.
    client = TestClient(app)

    # Step 2: open the page.
    logger.info("Act: opening /login")
    reply = client.get("/login")
    html = reply.text

    # Step 3: a real page, not the placeholder.
    assert reply.status_code == 200
    assert "Handler." not in html, "the page template is still the placeholder"
    logger.info("Assert: page language and title")
    assert '<html lang="en">' in html
    assert "<title>Sign in · TalkDesk</title>" in html
    logger.info("Assert: the form and its labels")
    assert '<form method="post" action="/login">' in html
    assert '<label for="email">' in html
    assert '<label for="password">' in html