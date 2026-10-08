"""Integration tests: a reviewer's decision, saved to the real database."""
import pytest

from utils.db import review_of, set_review


@pytest.mark.integration
def test_review_is_saved(api, database):
    """AC-17: a review is saved and returned, and no other talk changes."""
    original = review_of(database, 1)
    neighbour = review_of(database, 2)
    try:
        r = api.review_talk(1, status="accepted", score=9)
        assert r.status_code == 200
        assert (r.json()["status"], r.json()["score"]) == ("accepted", 9)

        fetched = api.get_talk(1).json()
        assert (fetched["status"], fetched["score"]) == ("accepted", 9)

        assert review_of(database, 2) == neighbour, "a different talk changed"
    finally:                                  # put talk 1 back as it was
        set_review(database, 1, *original)
