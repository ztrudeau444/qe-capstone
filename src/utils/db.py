"""Reading and resetting the database directly: the utils layer.

Tests use these to prove what did or did not change, and to put things back
afterwards, without going through the API they are testing.
"""
import psycopg


def talk_count(db_url):
    with psycopg.connect(db_url) as conn:
        return conn.execute("SELECT count(*) FROM talks").fetchone()[0]


def review_of(db_url, talk_id):
    """(status, score) of one talk."""
    with psycopg.connect(db_url) as conn:
        return conn.execute("SELECT status, score FROM talks WHERE id = %s",
                            (talk_id,)).fetchone()


def set_review(db_url, talk_id, status, score):
    with psycopg.connect(db_url) as conn:
        conn.execute("UPDATE talks SET status = %s, score = %s WHERE id = %s",
                     (status, score, talk_id))


def delete_talk(db_url, talk_id):
    with psycopg.connect(db_url) as conn:
        conn.execute("DELETE FROM talks WHERE id = %s", (talk_id,))
