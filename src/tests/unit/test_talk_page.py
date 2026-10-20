"""Unit tests: the talk details page (AC-14).

The home page linked each title to /api/talks/{id}, so a visitor who clicked
got raw JSON (found by the E2E test, 2026-10-20). These tests check the new
/talks/{id} web page without a database: get_talk and list_talks are swapped
for fakes.
"""
import importlib

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

app_module = importlib.import_module("talkdesk.app")
client = TestClient(app_module.app)

FAKE_TALK = {
    "id": 7, "title": "Testing <b>tips</b> & tricks", "abstract": "How we test.",
    "track": "testing", "status": "submitted",
    "speaker": {"id": 3, "name": "Ada", "email": "ada@example.com", "bio": ""},
    "created_at": "2026-10-20T10:00:00Z",
}


def fake_get_talk(talk_id):
    if talk_id == "7":
        return FAKE_TALK
    raise HTTPException(404, "talk not found")


@pytest.mark.unit
def test_home_page_links_titles_to_the_talk_page(monkeypatch):
    monkeypatch.setattr(app_module, "list_talks", lambda *a, **k: [FAKE_TALK])
    html = client.get("/").text
    assert 'href="/talks/7"' in html
    assert "/api/talks/" not in html


@pytest.mark.unit
def test_talk_page_shows_the_details(monkeypatch):
    monkeypatch.setattr(app_module, "get_talk", fake_get_talk)
    r = client.get("/talks/7")
    assert r.status_code == 200
    assert "<h2>Testing &lt;b&gt;tips&lt;/b&gt; &amp; tricks</h2>" in r.text
    assert "<title>Testing &lt;b&gt;tips&lt;/b&gt; &amp; tricks · TalkDesk</title>" in r.text
    for text in ("Ada", "testing", "submitted", "How we test.", 'href="/"'):
        assert text in r.text
    assert "ada@example.com" not in r.text


@pytest.mark.unit
@pytest.mark.parametrize("talk_id", ["999", "abc", "12345678901"])
def test_unknown_or_invalid_talk_gets_a_not_found_page(monkeypatch, talk_id):
    monkeypatch.setattr(app_module, "get_talk", fake_get_talk)
    r = client.get(f"/talks/{talk_id}")
    assert r.status_code == 404
    assert r.headers["content-type"].startswith("text/html")
    assert "Talk not found" in r.text