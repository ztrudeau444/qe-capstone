"""E2E: a visitor can browse to a talk (AC-14).

Drives a real browser (Chromium, via Playwright) against the running TalkDesk:
open the home page, click the first talk's title, and check that a talk page
shows that same title with its details.

Needs TalkDesk running (docker compose up -d --wait) and the browser installed
(python -m playwright install chromium). Run with:
    pytest src/tests/e2e --base-url http://localhost:8080
"""
import re

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.e2e
def test_visitor_browses_from_home_page_to_a_talk(page: Page):
    # Given the seeded database, a visitor opens the home page
    page.goto("/")
    first_link = page.locator("table tbody tr td a").first
    clicked_title = first_link.inner_text()

    # When they click the title of the first talk listed
    first_link.click()

    # Then they are on that talk's web page (not the JSON API)...
    expect(page).to_have_url(re.compile(r"://[^/]+/talks/\d+$"))
    # ...whose heading and tab title are the title they clicked...
    expect(page.locator("main h2")).to_have_text(clicked_title)
    expect(page).to_have_title(f"{clicked_title} · TalkDesk")
    # ...with the talk's full details
    for label in ("Speaker", "Track", "Status", "Abstract"):
        expect(page.locator("main")).to_contain_text(label)