"""Unit test: the home page escapes talk data (stored cross-site scripting).

The home page pasted each talk's title, speaker name, track and status straight
into its HTML. A talk titled <script>...</script> would then run in every
visitor's browser: stored cross-site scripting, found by reading the code on
2026-10-13 (ZAP's baseline scan only looks; it cannot find this).

monkeypatch swaps TalkDesk's list_talks for a fake one, so the test needs no
database and controls exactly what the page receives.
"""
import logging

import pytest
from fastapi.testclient import TestClient

import talkdesk.app as app_module

logger = logging.getLogger(__name__)

SCRIPT_TITLE = '<script>alert("xss")</script>'
TAGGED_NAME = "<b>Eve</b>"


@pytest.mark.unit
def test_home_page_shows_talk_data_as_text_not_html(monkeypatch):
    """A script in a title and a tag in a name are shown as text, never run.

    Steps:
      1. Arrange: replace list_talks with one fake talk carrying a script
         in its title and an HTML tag in its speaker's name.
      2. Act: open the home page.
      3. Assert: the raw script and tag are NOT in the page, and their
         escaped, harmless forms ARE (so the data is still shown).
    """
    # Step 1: a fake talk, as an attacker would submit it.
    fake_talk = {
        "id": 1,
        "title": SCRIPT_TITLE,
        "speaker": {"id": 1, "name": TAGGED_NAME},
        "track": "testing",
        "status": "submitted",
    }
    monkeypatch.setattr(app_module, "list_talks", lambda *args, **kwargs: [fake_talk])

    # Step 2: open the home page.
    logger.info("Act: opening the home page with a malicious talk title")
    reply = TestClient(app_module.app).get("/")
    assert reply.status_code == 200

    # Step 3: shown as text, not obeyed as HTML.
    logger.info("Assert: no raw script or tag in the page")
    assert SCRIPT_TITLE not in reply.text, "the title's script would run in the browser"
    assert TAGGED_NAME not in reply.text, "the speaker name's tag would be obeyed"
    logger.info("Assert: the escaped forms are there, so the data is still shown")
    assert "&lt;script&gt;alert(&quot;xss&quot;)&lt;/script&gt;" in reply.text
    assert "&lt;b&gt;Eve&lt;/b&gt;" in reply.text