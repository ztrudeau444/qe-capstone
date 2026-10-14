"""Unit tests: error replies expose no internals (AC-11, gap list #2, planted D-7).

The catch-all error handler sent visitors the exception name, its message and
the full traceback (with server file paths). Found by reading the code and
confirmed with curl: GET /api/talks/abc returned 4.5 KB of internals. The 500
reply also lacked the security headers every other reply carries.
/api/talks/abc fails at int("abc") before the database is touched, so these
tests need no database.
"""
from fastapi.testclient import TestClient

from talkdesk.app import app

# raise_server_exceptions=False: by default the test client re-raises the crash
# inside the test. A real visitor gets the 500 reply instead, so check that.
client = TestClient(app, raise_server_exceptions=False)


def crash_reply():
    r = client.get("/api/talks/abc")
    assert r.status_code == 500
    return r


def test_reply_has_no_exception_name_traceback_or_paths():
    text = crash_reply().text
    for leak in ("ValueError", "Traceback", "invalid literal", ".py", 'File \\"'):
        assert leak not in text, f"error reply leaks {leak!r}"


def test_reply_is_a_general_message_with_a_reference():
    body = crash_reply().json()
    assert set(body) == {"error", "reference"}
    assert "went wrong" in body["error"]
    assert len(body["reference"]) == 8


def test_error_reply_keeps_the_security_headers():
    r = crash_reply()
    assert r.headers.get("x-content-type-options") == "nosniff"
    assert "content-security-policy" in r.headers


def test_details_go_to_the_server_log_under_the_same_reference(caplog):
    ref = crash_reply().json().get("reference", "no reference in the reply")
    logged = [rec for rec in caplog.records if ref in rec.getMessage()]
    assert logged, "the server log has no entry for this reference"
    assert logged[0].exc_info, "the log entry has no traceback for the team"