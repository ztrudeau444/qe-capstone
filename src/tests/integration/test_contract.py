"""Contract test: the shape of a talk, as anything consuming the API relies on it.
If a field is renamed, removed or changes type, this fails before a consumer does."""
import pytest

TALK_FIELDS = {"id": int, "title": str, "abstract": str, "track": str,
               "status": str, "score": (int, type(None)), "speaker": dict,
               "created_at": str}
SPEAKER_FIELDS = {"id": int, "name": str, "email": str, "bio": (str, type(None))}


@pytest.mark.integration
def test_talk_detail_matches_the_contract(client):
    talk = client.get("/api/talks/1").json()

    assert set(talk) == set(TALK_FIELDS), "fields added or removed"
    for field, kind in TALK_FIELDS.items():
        assert isinstance(talk[field], kind), f"{field} changed type"

    assert set(talk["speaker"]) == set(SPEAKER_FIELDS)
    for field, kind in SPEAKER_FIELDS.items():
        assert isinstance(talk["speaker"][field], kind), f"speaker.{field} changed type"

    assert talk["created_at"].endswith("Z"), "timestamps are UTC"