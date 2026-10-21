"""Unit tests: only signed-in reviewers can review a talk (gap #1).

PATCH /api/talks/{id} never checked for a sign-in token, so anyone could
accept, reject or score any talk. These tests go through TalkDesk over HTTP
(TestClient), because the check happens at the door, before the review code
runs. A refused request never reaches the database (no_database proves it).
"""
import pytest
from fastapi.testclient import TestClient

from talkdesk.app import app

client = TestClient(app, raise_server_exceptions=False)
REVIEW = {"status": "accepted", "score": 9}


def sign_in():
    reply = client.post("/api/login", json={"email": "zoe@talkdesk.test", "password": "reviewer"})
    assert reply.status_code == 200
    return reply.json()["token"]


@pytest.mark.unit
def test_review_without_a_token_is_refused(no_database):
    reply = client.patch("/api/talks/1", json=REVIEW)
    assert reply.status_code == 401
    assert reply.json()["detail"] == "sign in to review talks"


@pytest.mark.unit
@pytest.mark.parametrize("header", [
    "Bearer made-up-token",
    "Bearer talkdesk-demo-token-not-a-credential",   # the old fixed token everyone could copy
    "made-up-token",                                 # no "Bearer" in front
])
def test_review_with_an_unknown_token_is_refused(no_database, header):
    reply = client.patch("/api/talks/1", json=REVIEW, headers={"Authorization": header})
    assert reply.status_code == 401


@pytest.mark.unit
def test_each_sign_in_gets_its_own_token():
    first, second = sign_in(), sign_in()
    assert first != second