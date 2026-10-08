"""Integration tests: the TalkDesk API and the database working together."""
import psycopg
import pytest


@pytest.mark.integration
def test_valid_talk_is_created(client, talk_count, database):
    """AC-01: a valid submission is saved; the database fills in the status;
    exactly one talk is added."""
    before = talk_count()
    r = client.post("/api/talks", json={
        "speaker_id": 27, "title": "Integration testing TalkDesk",
        "abstract": "", "track": "testing"})
    try:
        assert r.status_code == 201
        created = r.json()
        assert created["status"] == "submitted"   # set by the database, not the code
        fetched = client.get(f"/api/talks/{created['id']}").json()
        assert fetched["title"] == "Integration testing TalkDesk"
        assert fetched["track"] == "testing"
        assert talk_count() == before + 1
    finally:
        if r.status_code == 201:                    # leave the database as it was
            with psycopg.connect(database) as conn:
                conn.execute("DELETE FROM talks WHERE id = %s", (r.json()["id"],))


@pytest.mark.integration
def test_unknown_speaker_is_rejected(client, talk_count):
    """AC-04: a talk for a speaker who does not exist is rejected, and nothing is saved."""
    before = talk_count()
    r = client.post("/api/talks", json={
        "speaker_id": 999999, "title": "A valid title", "abstract": "", "track": "testing"})
    assert r.status_code == 404
    assert r.json()["detail"] == "speaker not found"
    assert talk_count() == before


@pytest.mark.integration
def test_listing_filters_by_track(client):
    """AC-07: only talks in the requested track, at most 100, in ascending ID order."""
    talks = client.get("/api/talks", params={"track": "testing"}).json()
    assert talks, "the seed data should contain talks in the testing track"
    assert all(t["track"] == "testing" for t in talks)
    assert len(talks) <= 100
    ids = [t["id"] for t in talks]
    assert ids == sorted(ids)


@pytest.mark.integration
def test_search_ignores_case(client):
    """AC-08: searching "flaky" finds titles containing "Flaky", in any case."""
    talks = client.get("/api/talks/search", params={"q": "flaky"}).json()
    assert talks, "the seed data should contain a talk about flaky tests"
    assert all("flaky" in t["title"].lower() for t in talks)
    assert any("Flaky" in t["title"] for t in talks)


@pytest.mark.integration
def test_unknown_talk_returns_not_found(client):
    """AC-09: a talk ID that does not exist returns 404 "talk not found"."""
    r = client.get("/api/talks/999999")
    assert r.status_code == 404
    assert r.json()["detail"] == "talk not found"