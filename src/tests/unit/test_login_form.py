"""Unit tests: the sign-in form answers with a page, not a raw 422 (gap list #17).

Found in the manual keyboard-only pass (2026-10-14): the form posted form data
to /api/login, which expects JSON, so the browser showed a raw 422 error page.
"""
from fastapi.testclient import TestClient

from talkdesk.app import app

client = TestClient(app)


def test_form_posts_to_the_web_route():
    assert 'action="/login"' in client.get("/login").text


def test_right_details_show_a_signed_in_page():
    r = client.post("/login", data={"email": "zoe@talkdesk.test", "password": "reviewer"})
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("text/html")
    assert "<title>Signed in · TalkDesk</title>" in r.text


def test_wrong_details_show_a_readable_error_and_a_way_back():
    r = client.post("/login", data={"email": "zoe@talkdesk.test", "password": "wrong"})
    assert r.status_code == 401
    assert r.headers["content-type"].startswith("text/html")
    assert "Email or password is incorrect" in r.text
    assert '<a href="/login">Try again</a>' in r.text


def test_api_login_still_takes_json():
    r = client.post("/api/login", json={"email": "zoe@talkdesk.test", "password": "reviewer"})
    assert r.status_code == 200
    assert "token" in r.json()