"""Test data: the utils layer.

valid_talk() returns a talk that passes every submission rule. A test changes
only the field it is about, so the reader sees what matters:
    valid_talk(speaker_id=999999)   # this test is about an unknown speaker
"""


def valid_talk(**overrides):
    talk = {"speaker_id": 27, "title": "A valid talk title",
            "abstract": "", "track": "testing"}
    talk.update(overrides)
    return talk
