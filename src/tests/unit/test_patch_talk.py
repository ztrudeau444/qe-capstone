"""Unit tests for reviewing a talk (patch_talk)."""
import pytest
from fastapi import HTTPException

from talkdesk.app import TalkPatch, patch_talk


@pytest.mark.unit
@pytest.mark.parametrize("score", [0, 11])
def test_score_outside_1_to_10_is_rejected(no_database, score):
    """AC-05 (closes D-9): the scores just outside 1-10 are rejected,
    and nothing is saved."""
    with pytest.raises(HTTPException) as error:
        patch_talk(1, TalkPatch(score=score))

    assert error.value.status_code == 400
    assert error.value.detail == "score must be between 1 and 10"


@pytest.mark.unit
def test_empty_update_is_rejected(no_database):
    """AC-06: an update with neither a status nor a score is rejected,
    and nothing is saved."""
    with pytest.raises(HTTPException) as error:
        patch_talk(1, TalkPatch())

    assert error.value.status_code == 400
    assert error.value.detail == "nothing to update"


@pytest.mark.unit
def test_invalid_status_is_rejected(no_database):
    """AC-16 (closes the R-05 finding): an unknown status is rejected,
    the message lists the allowed statuses, and nothing is saved."""
    with pytest.raises(HTTPException) as error:
        patch_talk(1, TalkPatch(status="maybe"))

    assert error.value.status_code == 400
    for status in ("accepted", "rejected", "submitted"):
        assert status in error.value.detail