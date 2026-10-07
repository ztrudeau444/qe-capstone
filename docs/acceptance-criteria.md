# Acceptance Criteria

System Under Test: **TalkDesk** (Python / FastAPI). Week 1. At least eight, at least three in full three-clause form.

**Three-clause prose, not Gherkin.** Week 1 deliberately has no specification
DSL — the tooling decision comes in Week 2 §2.9 once you have E2E automation
for it to wrap. Right now you are learning to *state* a behaviour precisely.

## The form

> **Given** some starting state
> **When** something happens
> **Then** an observable outcome, and nothing else changed

The last clause is the one people skip and the one that catches defects.

Criteria state what TalkDesk **should** do. Where it currently does not, the
criterion is kept and marked **known gap**: a failing test against a written
criterion is how a defect gets found.

## Criteria

### AC-01 — Valid talk is created

**Given** speaker 27 exists
**When** a talk is submitted with a non-blank title, an abstract and the track "testing"
**Then** the reply is 201 with a new ID and status "submitted", fetching that ID returns the same title and track, and no other talk has changed

| | |
|---|---|
| **Type** | Functional |
| **Test layer** | Integration |
| **Why that layer** | The new ID, the status "submitted" and the creation date are filled in by the database; a unit test replaces the database with a stand-in, so it cannot tell whether the real one fills them in correctly. |
| **Test** | |
| **Status** | Not started |

### AC-02 — Blank title is rejected

**Given** speaker 27 exists
**When** a talk is submitted with a title made only of spaces
**Then** the reply is 400 with the message "title is required", and no talk is created

| | |
|---|---|
| **Type** | Functional |
| **Test layer** | Unit |
| **Why that layer** | "A title must not be blank" is a rule, checked in the code before the database is touched. |
| **Test** | `src/tests/unit/test_create_talk.py::test_blank_title_is_rejected` |
| **Status** | Green |

### AC-03 — Invalid track is rejected

**Given** speaker 27 exists
**When** a talk is submitted with the track "cooking"
**Then** the reply is 400 and the message lists the allowed tracks (architecture, culture, delivery, testing), and no talk is created

| | |
|---|---|
| **Type** | Functional |
| **Test layer** | Unit |
| **Why that layer** | The list of allowed tracks is a rule held in the code. |
| **Test** | `src/tests/unit/test_create_talk.py::test_invalid_track_is_rejected` |
| **Status** | Green |

### AC-04 — Unknown speaker is rejected

**Given** no speaker exists with ID 999999
**When** a talk is submitted for speaker 999999 with a valid title and track
**Then** the reply is 404 with the message "speaker not found", and no talk is created

| | |
|---|---|
| **Type** | Functional |
| **Test layer** | Integration |
| **Why that layer** | Whether a speaker exists is the database's answer; with a stand-in, the test would only check the answer the stand-in was told to give. |
| **Test** | |
| **Status** | Not started |

### AC-05 — Score outside 1–10 is rejected

**Given** an existing talk with a score of 7
**When** a reviewer updates its score to 11
**Then** the reply is 400 with the message "score must be between 1 and 10", and the talk's score is still 7

| | |
|---|---|
| **Type** | Functional |
| **Test layer** | Unit |
| **Why that layer** | "Scores must be 1–10" is a rule, checked before the database is touched. |
| **Test** | `src/tests/unit/test_patch_talk.py::test_score_outside_1_to_10_is_rejected` |
| **Status** | Green |

### AC-06 — Empty update is rejected

**Given** an existing talk
**When** a reviewer sends an update containing neither a status nor a score
**Then** the reply is 400 with the message "nothing to update", and the talk is unchanged

| | |
|---|---|
| **Type** | Functional |
| **Test layer** | Unit |
| **Why that layer** | Deciding that an empty update is invalid is logic in the code. |
| **Test** | `src/tests/unit/test_patch_talk.py::test_empty_update_is_rejected` |
| **Status** | Green |

### AC-07 — Listing filters by track

**Given** the seeded database, which holds talks in all four tracks
**When** the list of talks is requested with the track "testing"
**Then** every talk returned has the track "testing", no more than 100 are returned, and they are in ascending ID order

| | |
|---|---|
| **Type** | Functional |
| **Test layer** | Integration |
| **Why that layer** | The filtering, limit and ordering are done by the SQL query; a stand-in database would return whatever the test fed it, so a broken query would still pass. |
| **Test** | |
| **Status** | Not started |

### AC-08 — Search matches title words regardless of case

**Given** a talk exists whose title contains "Flaky Tests"
**When** talks are searched for "flaky"
**Then** that talk is in the results, and every result's title contains "flaky" in some combination of upper and lower case

| | |
|---|---|
| **Type** | Functional |
| **Test layer** | Integration |
| **Why that layer** | Case-insensitive matching is done by the database (`ILIKE`), which a unit test replaces. |
| **Test** | |
| **Status** | Not started |

### AC-09 — Unknown talk ID returns "not found"

**Given** no talk exists with ID 999999
**When** talk 999999 is requested
**Then** the reply is 404 with the message "talk not found"

| | |
|---|---|
| **Type** | Functional |
| **Test layer** | Integration |
| **Why that layer** | "This talk does not exist" is only known by asking the real database; a stand-in would only report what it was told to. |
| **Test** | |
| **Status** | Not started |

### AC-10 — Reviewer sign-in

**Given** a reviewer with an `@talkdesk.test` email address
**When** they sign in with the correct password, and separately with a wrong one
**Then** the correct password returns a token, and the wrong one returns 401 "invalid credentials" with no token

| | |
|---|---|
| **Type** | Functional |
| **Test layer** | Unit |
| **Why that layer** | The sign-in check is pure logic in the code and never uses the database. |
| **Test** | `src/tests/unit/test_login.py::test_correct_password_returns_token, test_wrong_password_is_rejected` |
| **Status** | Green |

### AC-11 — Errors never expose internal details (known gap)

**Given** any request that causes an unexpected error (for example, requesting talk `abc`, which is not a number)
**When** the system replies
**Then** the reply contains a general error message only: no exception name, no traceback and no file paths

| | |
|---|---|
| **Type** | Non-functional (security) |
| **Test layer** | Unit |
| **Why that layer** | The error handler is a single function; a test can hand it an error and inspect what it returns. |
| **Test** | |
| **Status** | Not started — known gap: TalkDesk currently returns the full traceback |

### AC-12 — Talk list stays fast under load

**Given** the seeded database of 50,000 talks
**When** the list of talks is requested repeatedly under the Week 3 load profile
**Then** the 95th-percentile response time is 500 ms or less, and fewer than 1% of requests fail

| | |
|---|---|
| **Type** | Non-functional (performance) |
| **Test layer** | System level — Week 3 load test |
| **Why that layer** | Response time only exists for the running system as a whole, so no lower layer can measure it. |
| **Test** | |
| **Status** | Not started |

### AC-13 — The sign-in page is accessible (known gap)

**Given** the sign-in page is loaded in a browser
**When** it is scanned with the Week 3 accessibility tools
**Then** the score is 95 or higher, with no critical or serious issues, and the form can be completed using the keyboard alone

| | |
|---|---|
| **Type** | Non-functional (accessibility) |
| **Test layer** | E2E — Week 3 |
| **Why that layer** | Accessibility is a property of the rendered page, which only exists at the top layer (the §3.8 exception). |
| **Test** | |
| **Status** | Not started — known gap: the web pages currently show only "Handler." |

### AC-14 — A visitor can browse to a talk (known gap)

**Given** the seeded database
**When** a visitor opens the home page and clicks the title of the first talk listed
**Then** they see that talk's full details, and the title matches the one they clicked

| | |
|---|---|
| **Type** | Functional |
| **Test layer** | E2E |
| **Why that layer** | This checks that the page, the link and the API are wired together, which only exists at the top; an integration test can prove the API returns a talk, but not that the link on the page points to it. |
| **Test** | |
| **Status** | Not started — known gap: the home page currently shows only "Handler." |

### AC-15 — Over-long title is rejected

**Given** speaker 27 exists
**When** a talk is submitted with a title of 201 characters
**Then** the reply is 400 with the message "title must be 200 characters or fewer", and no talk is created

| | |
|---|---|
| **Type** | Functional |
| **Test layer** | Unit |
| **Why that layer** | A length limit is a rule, checked in the code before the database is touched. |
| **Test** | `src/tests/unit/test_create_talk.py::test_title_over_200_characters_is_rejected` |
| **Status** | Green |

## Traceability

Every functional criterion must reach 100% coverage by the Week 4 exit gate.

| ID | Criterion | Layer | Test | Green |
|---|---|---|---|---|
| AC-01 | Valid talk is created | Integration | | ☐ |
| AC-02 | Blank title rejected | Unit | test_blank_title_is_rejected | ☒ |
| AC-03 | Invalid track rejected | Unit | test_invalid_track_is_rejected | ☒ |
| AC-04 | Unknown speaker rejected | Integration | | ☐ |
| AC-05 | Score outside 1–10 rejected | Unit | test_score_outside_1_to_10_is_rejected | ☒ |
| AC-06 | Empty update rejected | Unit | test_empty_update_is_rejected | ☒ |
| AC-07 | List filters by track | Integration | | ☐ |
| AC-08 | Search is case-insensitive | Integration | | ☐ |
| AC-09 | Unknown talk ID → 404 | Integration | | ☐ |
| AC-10 | Reviewer sign-in | Unit | test_correct_password_returns_token, test_wrong_password_is_rejected | ☒ |
| AC-11 | Errors expose no internals (NF, known gap) | Unit | | ☐ |
| AC-12 | List p95 ≤ 500 ms under load (NF) | System (Week 3) | | ☐ |
| AC-13 | Sign-in page accessible (NF, known gap) | E2E (Week 3) | | ☐ |
| AC-14 | Visitor browses to a talk (known gap) | E2E | | ☐ |
| AC-15 | Over-long title rejected | Unit | test_title_over_200_characters_is_rejected | ☒ |
