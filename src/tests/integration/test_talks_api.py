"""Integration tests: the TalkDesk API and the database working together."""
import pytest

from utils.db import delete_talk, talk_count
from utils.talk_data import valid_talk


@pytest.mark.integration
def test_valid_talk_is_created(api, database):
    """AC-01: a valid submission is saved; the database fills in the status;
    exactly one talk is added."""
    before = talk_count(database)
    r = api.submit_talk(**valid_talk(title="Integration testing TalkDesk"))
    try:
        assert r.status_code == 201
        created = r.json()
        assert created["status"] == "submitted"   # set by the database, not the code
        fetched = api.get_talk(created["id"]).json()
        assert fetched["title"] == "Integration testing TalkDesk"
        assert fetched["track"] == "testing"
        assert talk_count(database) == before + 1
    finally:
        if r.status_code == 201:                    # leave the database as it was
            delete_talk(database, r.json()["id"])


@pytest.mark.integration
def test_unknown_speaker_is_rejected(api, database):
    """AC-04: a talk for a speaker who does not exist is rejected, and nothing is saved."""
    before = talk_count(database)
    r = api.submit_talk(**valid_talk(speaker_id=999999))
    assert r.status_code == 404
    assert r.json()["detail"] == "speaker not found"
    assert talk_count(database) == before


@pytest.mark.integration
def test_listing_filters_by_track(api):
    """AC-07: only talks in the requested track, at most 100, in ascending ID order."""
    talks = api.list_talks(track="testing").json()
    assert talks, "the seed data should contain talks in the testing track"
    assert all(t["track"] == "testing" for t in talks)
    assert len(talks) <= 100
    ids = [t["id"] for t in talks]
    assert ids == sorted(ids)


@pytest.mark.integration
def test_search_ignores_case(api):
    """AC-08: searching "flaky" finds titles containing "Flaky", in any case."""
    talks = api.search_talks("flaky").json()
    assert talks, "the seed data should contain a talk about flaky tests"
    assert all("flaky" in t["title"].lower() for t in talks)
    assert any("Flaky" in t["title"] for t in talks)


@pytest.mark.integration
def test_unknown_talk_returns_not_found(api):
    """AC-09: a talk ID that does not exist returns 404 "talk not found"."""
    r = api.get_talk(999999)
    assert r.status_code == 404
    assert r.json()["detail"] == "talk not found"
