"""Unit tests for reviewer sign-in (login)."""
import pytest
from fastapi import HTTPException

from talkdesk.app import Login, login


@pytest.mark.unit
def test_correct_password_returns_token():
    """AC-10: a reviewer with the correct password gets a token."""
    result = login(Login(email="reviewer@talkdesk.test", password="reviewer"))

    assert "token" in result


@pytest.mark.unit
def test_wrong_password_is_rejected():
    """AC-10: a wrong password is rejected with 401 and no token."""
    with pytest.raises(HTTPException) as error:
        login(Login(email="reviewer@talkdesk.test", password="wrong"))

    assert error.value.status_code == 401
    assert error.value.detail == "invalid credentials"
