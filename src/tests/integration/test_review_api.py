"""Integration tests: a reviewer's decision, saved to the real database."""
import psycopg
import pytest


@pytest.mark.integration
def test_review_is_saved(client, database):
    """AC-17: a review is saved and returned, and no other talk changes."""
    with psycopg.connect(database) as conn:
        original = conn.execute("SELECT status, score FROM talks WHERE id = 1").fetchone()
        neighbour = conn.execute("SELECT status, score FROM talks WHERE id = 2").fetchone()
    try:
        r = client.patch("/api/talks/1", json={"status": "accepted", "score": 9})
        assert r.status_code == 200
        assert (r.json()["status"], r.json()["score"]) == ("accepted", 9)

        fetched = client.get("/api/talks/1").json()
        assert (fetched["status"], fetched["score"]) == ("accepted", 9)

        with psycopg.connect(database) as conn:
            after = conn.execute("SELECT status, score FROM talks WHERE id = 2").fetchone()
        assert after == neighbour, "a different talk changed"
    finally:                                  # put talk 1 back as it was
        with psycopg.connect(database) as conn:
            conn.execute("UPDATE talks SET status = %s, score = %s WHERE id = 1", original)