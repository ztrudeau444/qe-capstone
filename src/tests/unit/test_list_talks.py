"""Unit tests: the talk list shows the newest talks first (gap list #21).

list_talks() sorted by id, oldest first, and kept 100, so with 50,000 seeded
talks a new submission (id 50001) never appeared on the home page or in
GET /api/talks. Found during load testing; confirmed 2026-10-14 with a talk
submitted through the new /submit form.
The database is replaced by a fake that records the SQL it is given, so these
tests need no database. The real-database check is in docs/evidence/week4/.
"""
import talkdesk.app as talkdesk_app


class FakeConn:
    """Stands in for the database connection and remembers the last query."""
    def __init__(self):
        self.sql = None

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def execute(self, sql, args=()):
        self.sql = sql
        return self

    def fetchall(self):
        return []


def run_list_talks(monkeypatch, **filters):
    conn = FakeConn()
    monkeypatch.setattr(talkdesk_app, "db", lambda: conn)
    talkdesk_app.list_talks(**filters)
    return conn.sql


def test_newest_talks_come_first(monkeypatch):
    sql = run_list_talks(monkeypatch)
    assert "ORDER BY t.id DESC" in sql, "oldest talks first: new ones never show"
    assert "LIMIT 100" in sql


def test_filters_still_apply_with_newest_first(monkeypatch):
    sql = run_list_talks(monkeypatch, track="testing", status="submitted")
    assert "t.track = %s" in sql and "t.status = %s" in sql
    assert sql.rstrip().endswith("ORDER BY t.id DESC LIMIT 100")