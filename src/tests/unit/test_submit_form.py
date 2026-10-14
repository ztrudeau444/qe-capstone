"""Unit tests: the /submit page shows a real talk form, not "Handler." (gap list #18).

The page body was the placeholder "Handler.", so speakers could not submit a
talk from the website; only the JSON API at /api/talks worked.
These tests need no database: they only read the page.
"""
from fastapi import HTTPException
from fastapi.testclient import TestClient

import talkdesk.app as talkdesk_app
from talkdesk.app import app

client = TestClient(app)


def submit_page():
    r = client.get("/submit")
    assert r.status_code == 200
    return r.text


def test_page_is_not_the_placeholder():
    assert "Handler." not in submit_page()


def test_form_posts_to_the_web_route():
    assert '<form method="post" action="/submit">' in submit_page()


def test_every_field_has_a_label():
    html = submit_page()
    for field in ("speaker_id", "title", "abstract", "track"):
        assert f'<label for="{field}">' in html, f"no label for {field}"
        assert f'name="{field}"' in html, f"no {field} field"


def test_abstract_is_a_text_area():
    assert '<textarea id="abstract" name="abstract"' in submit_page()


def test_has_a_submit_button():
    assert '<button type="submit">' in submit_page()



# ── Plate 2: sending the form (POST /submit) ──────────────────────────────
# A good submission is saved by create_talk(), the same code as the JSON API,
# so the form and the API follow the same rules. Rule-breaking input is
# rejected before the database is touched, so those tests use the real code.
# Tests that would reach the database swap in a fake create_talk instead.

GOOD = {"speaker_id": "1", "title": "Testing in the kitchen",
        "abstract": "Mise en place for QA.", "track": "testing"}


def fake_save(saved):
    """A stand-in for create_talk that records what it was given."""
    def create_talk(body):
        saved.append(body)
        return {"id": 99, "title": body.title}
    return create_talk


def test_good_submission_saves_and_says_thanks(monkeypatch):
    saved = []
    monkeypatch.setattr(talkdesk_app, "create_talk", fake_save(saved))
    r = client.post("/submit", data=GOOD)
    assert r.status_code == 201
    assert r.headers["content-type"].startswith("text/html")
    assert "<title>Talk submitted · TalkDesk</title>" in r.text
    assert len(saved) == 1, "the talk was not handed to create_talk"
    assert saved[0].speaker_id == 1 and saved[0].track == "testing"


def test_thanks_page_escapes_the_title(monkeypatch):
    monkeypatch.setattr(talkdesk_app, "create_talk", fake_save([]))
    r = client.post("/submit", data={**GOOD, "title": "<script>alert(1)</script>"})
    assert "<script>alert(1)</script>" not in r.text
    assert "&lt;script&gt;" in r.text


def test_empty_title_shows_a_readable_error_and_a_way_back():
    r = client.post("/submit", data={**GOOD, "title": "   "})
    assert r.status_code == 400
    assert r.headers["content-type"].startswith("text/html")
    assert "title is required" in r.text
    assert '<a href="/submit">Try again</a>' in r.text


def test_unknown_track_shows_a_readable_error():
    r = client.post("/submit", data={**GOOD, "track": "cooking"})
    assert r.status_code == 400
    assert "track must be one of" in r.text


def test_speaker_id_that_is_not_a_number_shows_a_readable_error():
    r = client.post("/submit", data={**GOOD, "speaker_id": "abc"})
    assert r.status_code == 400
    assert "Speaker ID must be a number" in r.text


def test_unknown_speaker_shows_a_readable_error(monkeypatch):
    def no_such_speaker(body):
        raise HTTPException(404, "speaker not found")
    monkeypatch.setattr(talkdesk_app, "create_talk", no_such_speaker)
    r = client.post("/submit", data=GOOD)
    assert r.status_code == 404
    assert "speaker not found" in r.text
    assert '<a href="/submit">Try again</a>' in r.text