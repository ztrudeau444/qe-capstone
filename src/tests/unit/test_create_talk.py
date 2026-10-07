"""Unit tests for submitting a talk (create_talk)."""
import pytest
from fastapi import HTTPException

import talkdesk.app as app_module
from talkdesk.app import NewTalk, create_talk


@pytest.mark.unit
def test_title_over_200_characters_is_rejected(monkeypatch):
    """AC-15: a 201-character title is rejected, and no talk is created."""
    # A stand-in for the database that fails loudly if it is ever used.
    # That proves the "and no talk is created" part of the criterion.
    def database_must_not_be_touched():
        raise AssertionError("the database must not be touched")

    monkeypatch.setattr(app_module, "db", database_must_not_be_touched)

    body = NewTalk(speaker_id=27, title="x" * 201, abstract="", track="testing")

    with pytest.raises(HTTPException) as error:
        create_talk(body)

    assert error.value.status_code == 400
    assert error.value.detail == "title must be 200 characters or fewer"


@pytest.mark.unit
def test_blank_title_is_rejected(no_database):
    """AC-02: a title of only spaces is rejected, and no talk is created."""
    body = NewTalk(speaker_id=27, title="   ", abstract="", track="testing")

    with pytest.raises(HTTPException) as error:
        create_talk(body)

    assert error.value.status_code == 400
    assert error.value.detail == "title is required"


@pytest.mark.unit
def test_invalid_track_is_rejected(no_database):
    """AC-03: an unknown track is rejected, the message lists the allowed
    tracks, and no talk is created."""
    body = NewTalk(speaker_id=27, title="A valid title", abstract="", track="cooking")

    with pytest.raises(HTTPException) as error:
        create_talk(body)

    assert error.value.status_code == 400
    for track in ("architecture", "culture", "delivery", "testing"):
        assert track in error.value.detail
