# Acceptance Criteria — TalkDesk

System Under Test: TalkDesk (Python / FastAPI) · Week 1, Stage 2

Each criterion is written as Given / When / Then, marked functional (F) or
non-functional (NF), and mapped to the lowest test layer that could catch a
failure (Reader §3.8). Criteria state what the system **should** do. Where
TalkDesk does not currently do it, the criterion is kept and flagged as a
**known gap**: a failing test against a written criterion is how a defect
gets found.

---

## Submitting talks

### AC-1 · Valid talk is created (F · integration)

- **Given** speaker 27 exists
- **When** a talk is submitted with a non-blank title, an abstract and the track "testing"
- **Then** the reply is 201 with a new ID and status "submitted", fetching that ID returns the same title and track, and no other talk has changed.

**Layer:** integration. The new ID, the status "submitted" and the creation date are filled in by the database, not the code.
**Why not unit:** a unit test replaces the database with a stand-in, so it cannot tell whether the real database fills those in correctly.

### AC-2 · Blank title is rejected (F · unit)

- **Given** speaker 27 exists
- **When** a talk is submitted with a title made only of spaces
- **Then** the reply is 400 with the message "title is required", and no talk is created.

**Layer:** unit. "A title must not be blank" is a rule, checked in the code before the database is touched.

### AC-3 · Invalid track is rejected (F · unit)

- **Given** speaker 27 exists
- **When** a talk is submitted with the track "cooking"
- **Then** the reply is 400 and the message lists the allowed tracks (architecture, culture, delivery, testing), and no talk is created.

**Layer:** unit. The list of allowed tracks is a rule held in the code.

### AC-4 · Unknown speaker is rejected (F · integration)

- **Given** no speaker exists with ID 999999
- **When** a talk is submitted for speaker 999999 with a valid title and track
- **Then** the reply is 404 with the message "speaker not found", and no talk is created.

**Layer:** integration. Whether a speaker exists is the database's answer.
**Why not unit:** with the database replaced by a stand-in, the test would only check the answer the stand-in was told to give.

---

## Reviewing talks

### AC-5 · Score outside 1–10 is rejected (F · unit)

- **Given** an existing talk with a score of 7
- **When** a reviewer updates its score to 11
- **Then** the reply is 400 with the message "score must be between 1 and 10", and the talk's score is still 7.

**Layer:** unit. "Scores must be 1–10" is a rule, checked before the database is touched.

### AC-6 · An update with nothing in it is rejected (F · unit)

- **Given** an existing talk
- **When** a reviewer sends an update containing neither a status nor a score
- **Then** the reply is 400 with the message "nothing to update", and the talk is unchanged.

**Layer:** unit. Deciding that an empty update is invalid is logic in the code.

---

## Finding talks

### AC-7 · Listing filters by track (F · integration)

- **Given** the seeded database, which holds talks in all four tracks
- **When** the list of talks is requested with the track "testing"
- **Then** every talk returned has the track "testing", no more than 100 are returned, and they are in ascending ID order.

**Layer:** integration. The filtering, limit and ordering are done by the SQL query against the real database.
**Why not unit:** a stand-in database would return whatever the test fed it, so a broken query would still pass.

### AC-8 · Search matches title words regardless of case (F · integration)

- **Given** a talk exists whose title contains "Flaky Tests"
- **When** talks are searched for "flaky"
- **Then** that talk is in the results, and every result's title contains "flaky" in some combination of upper and lower case.

**Layer:** integration. Case-insensitive matching is done by the database (`ILIKE`), not by the code.
**Why not unit:** the matching rule lives in the database, which a unit test replaces.

### AC-9 · Unknown talk ID returns "not found" (F · integration)

- **Given** no talk exists with ID 999999
- **When** talk 999999 is requested
- **Then** the reply is 404 with the message "talk not found".

**Layer:** integration. "This talk does not exist" is only known by asking the real database.
**Why not unit:** the stand-in would only report what it was told to.

---

## Signing in

### AC-10 · Reviewer sign-in (F · unit)

- **Given** a reviewer with an `@talkdesk.test` email address
- **When** they sign in with the correct password, and separately with a wrong one
- **Then** the correct password returns a token, and the wrong one returns 401 "invalid credentials" with no token.

**Layer:** unit. The sign-in check is pure logic in the code and never uses the database.

---

## Non-functional

### AC-11 · Errors never expose internal details (NF · security · unit) — known gap

- **Given** any request that causes an unexpected error (for example, requesting talk `abc`, which is not a number)
- **When** the system replies
- **Then** the reply contains a general error message only: no exception name, no traceback and no file paths.

**Layer:** unit. The error handler is a single function; a test can hand it an error and inspect what it returns.
**Known gap:** TalkDesk currently returns the full traceback. Expected to fail.

### AC-12 · Talk list stays fast under load (NF · performance · system level, Week 3)

- **Given** the seeded database of 50,000 talks
- **When** the list of talks is requested repeatedly under the Week 3 load profile
- **Then** the 95th-percentile response time is 500 ms or less, and fewer than 1% of requests fail.

**Layer:** system level, measured by the Week 3 load test. Response time only exists for the running system as a whole, so no lower layer can measure it.

### AC-13 · The sign-in page is accessible (NF · accessibility · end-to-end, Week 3) — known gap

- **Given** the sign-in page is loaded in a browser
- **When** it is scanned with the Week 3 accessibility tools
- **Then** the score is 95 or higher, with no critical or serious issues, and the form can be completed using the keyboard alone.

**Layer:** end-to-end. Accessibility is a property of the rendered page, which only exists at the top layer (the §3.8 exception).
**Known gap:** the web pages currently show only "Handler.", so there is no form to scan yet.

---

## End-to-end journey

### AC-14 · A visitor can browse to a talk (F · end-to-end) — known gap

- **Given** the seeded database
- **When** a visitor opens the home page and clicks the title of the first talk listed
- **Then** they see that talk's full details, and the title matches the one they clicked.

**Layer:** end-to-end. This checks that the page, the link and the API are wired together, which only exists at the top.
**Why not integration:** an integration test can prove the API returns a talk, but not that the link on the page points to it.
**Known gap:** the home page currently shows only "Handler."

---

## Traceability table

| # | Criterion (short form) | F / NF | Layer that should test it | Test name | Status |
|---|---|---|---|---|---|
| 1 | Valid talk is created | F | Integration | | ☐ |
| 2 | Blank title rejected | F | Unit | | ☐ |
| 3 | Invalid track rejected | F | Unit | | ☐ |
| 4 | Unknown speaker rejected | F | Integration | | ☐ |
| 5 | Score outside 1–10 rejected | F | Unit | | ☐ |
| 6 | Empty update rejected | F | Unit | | ☐ |
| 7 | List filters by track | F | Integration | | ☐ |
| 8 | Search is case-insensitive | F | Integration | | ☐ |
| 9 | Unknown talk ID → 404 | F | Integration | | ☐ |
| 10 | Reviewer sign-in | F | Unit | | ☐ |
| 11 | Errors expose no internals | NF | Unit | | ☐ known gap |
| 12 | List p95 ≤ 500 ms under load | NF | System (Week 3) | | ☐ |
| 13 | Sign-in page accessible | NF | End-to-end (Week 3) | | ☐ known gap |
| 14 | Visitor browses to a talk | F | End-to-end | | ☐ known gap |

Rows with no test after Week 2: ______ · and why: ____________________
