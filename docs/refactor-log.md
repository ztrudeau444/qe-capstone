# Refactor Log

Week 1 onward. The Clean Code & Architecture mark (15%) is read from this file
across all four weeks — not from your Week 4 code.

One entry per refactor. A refactor with no before/after is an assertion, not
evidence.

---

## R-01 — Name the title length limit

| | |
|---|---|
| **Date** | 2026-10-07 · commit `ab25830` |
| **Principle** | Other: meaningful names (no magic numbers) |
| **Trigger** | The TDD green step (`9631f9b`) wrote the limit `200` twice, once in the check and once in the error message, with nothing saying what it meant. |

**Before**

```python
if len(body.title) > 200:
    raise HTTPException(400, "title must be 200 characters or fewer")
```

**After**

```python
MAX_TITLE_LENGTH = 200          # beside TRACKS and STATUSES, with the other rules

if len(body.title) > MAX_TITLE_LENGTH:
    raise HTTPException(400, f"title must be {MAX_TITLE_LENGTH} characters or fewer")
```

**What it bought**

The limit is changed in one place, and the error message can no longer
disagree with the check it describes.

**Tests that proved it was safe**

`test_title_over_200_characters_is_rejected`: green before and after. This was
the refactor step of the AC-15 TDD cycle (`05fe645` red, `9631f9b` green).

---

## R-02 — Use the shared `no_database` fixture

| | |
|---|---|
| **Date** | 2026-10-07 · commit `86eb380` |
| **Principle** | DRY |
| **Trigger** | The first unit test built its own database stand-in in six lines. Every later unit test needed the same guarantee, so the block would have been copied into each one. |

**Before**

```python
def test_title_over_200_characters_is_rejected(monkeypatch):
    def database_must_not_be_touched():
        raise AssertionError("the database must not be touched")

    monkeypatch.setattr(app_module, "db", database_must_not_be_touched)
    ...
```

**After**

```python
# src/tests/unit/conftest.py, defined once
@pytest.fixture
def no_database(monkeypatch): ...

# each test just asks for it by name
def test_title_over_200_characters_is_rejected(no_database):
    ...
```

**What it bought**

Every unit test gets the "the database must not be touched" guarantee by
naming one fixture, and if the guard ever needs to change, it changes in one
file.

**Tests that proved it was safe**

All 8 unit tests green before and after, including the refactored test itself.

---

## R-03 — Replace meaningless docstrings

| | |
|---|---|
| **Date** | 2026-10-07 · commit `a8bc851` |
| **Principle** | Other: comments should say what the code does |
| **Trigger** | The module and nine functions all had the identical docstring `"""Handler."""`, which told a reader nothing and was the same for code doing completely different jobs. |

**Before**

```python
def create_talk(body: NewTalk):
    """Handler."""

async def verbose_error_handler(request, exc):
    """Handler."""
```

**After**

```python
def create_talk(body: NewTalk):
    """Submit a new talk. Rule-breaking input is rejected before anything is saved."""

async def verbose_error_handler(request, exc):
    """Turn any unhandled error into a 500 reply.
    Known gap (AC-11, D-7): the reply includes internal details."""
```

**What it bought**

A reader learns what each function is for without reading its body, and the
known gap D-7 is now recorded at the exact place it lives. `PAGE = """Handler."""`
and the submit page's content were deliberately left alone: those strings are
what the pages display, so changing them would change behaviour.

**Tests that proved it was safe**

All 8 unit tests green before and after. Docstrings cannot change behaviour;
the suite confirms nothing else changed with them.

---

## R-04 — Split the submission rules out of `create_talk`

| | |
|---|---|
| **Date** | 2026-10-07 · commit `1f8d8bd` |
| **Principle** | SRP |
| **Trigger** | `create_talk` had two reasons to change: the submission rules (blank title, length, track) and the database write. Adding the AC-15 length rule meant editing a function that also owns SQL. |

**Before**

```python
def create_talk(body: NewTalk):
    if not body.title.strip():
        raise HTTPException(400, "title is required")
    if len(body.title) > MAX_TITLE_LENGTH:
        raise HTTPException(400, ...)
    if body.track not in TRACKS:
        raise HTTPException(400, ...)
    with db() as c:
        ...                      # speaker lookup and INSERT
```

**After**

```python
def validate_new_talk(body: NewTalk) -> None:
    """The submission rules. Raises a 400 for the first rule broken."""
    if not body.title.strip(): ...
    if len(body.title) > MAX_TITLE_LENGTH: ...
    if body.track not in TRACKS: ...

def create_talk(body: NewTalk):
    validate_new_talk(body)
    with db() as c:
        ...                      # unchanged
```

**What it bought**

A new submission rule is added in `validate_new_talk` without touching database
code, and the rules can now be tested by calling `validate_new_talk` directly,
with no database stand-in at all.

**Tests that proved it was safe**

`test_blank_title_is_rejected`, `test_invalid_track_is_rejected` and
`test_title_over_200_characters_is_rejected`: green before and after.

---

## R-05 — Split the review rules out of `patch_talk`

| | |
|---|---|
| **Date** | 2026-10-07 · commit `5d80e42` |
| **Principle** | SRP |
| **Trigger** | Same shape as R-04. `patch_talk` mixed the review rules with building and running the UPDATE, and the "nothing to update" rule was hidden inside the SQL-building code as `if not sets`. |

**Before**

```python
def patch_talk(talk_id: int, body: TalkPatch):
    if body.status is not None and body.status not in STATUSES: ...
    if body.score is not None and not (1 <= body.score <= 10): ...
    sets, args = [], []
    ...                          # build the SET clause
    if not sets:
        raise HTTPException(400, "nothing to update")
```

**After**

```python
def validate_talk_patch(body: TalkPatch) -> None:
    """The review rules. Raises a 400 for the first rule broken."""
    if body.status is not None and body.status not in STATUSES: ...
    if body.score is not None and not (1 <= body.score <= 10): ...
    if body.status is None and body.score is None:
        raise HTTPException(400, "nothing to update")

def patch_talk(talk_id: int, body: TalkPatch):
    validate_talk_patch(body)
    sets, args = [], []
    ...                          # unchanged
```

**What it bought**

All three review rules are in one place, and "nothing to update" is stated as
the rule it is ("neither a status nor a score was sent") instead of being
inferred from an empty SQL list. The outcome is identical for every input.

**Tests that proved it was safe**

`test_score_outside_1_to_10_is_rejected` (0 and 11) and
`test_empty_update_is_rejected`: green before and after.
**Finding:** the invalid-status rule ("status must be one of ...") has no test.
It was moved without a safety net, and is the next unit test to write.

---

## R-06 — Move the shared setup into `base/`

| | |
|---|---|
| **Date** | 2026-10-08 · commit `061db29` |
| **Principle** | SRP / DRY |
| **Trigger** | The `database` and `client` fixtures lived in `src/tests/integration/conftest.py`, inside the tests folder. Week 2 §3.3 puts shared setup in its own `base/` layer, and E2E and smoke tests will need the same `database`. |

**Before**

```python
# src/tests/integration/conftest.py
@pytest.fixture(scope="session")
def database(): ...
@pytest.fixture
def client(database, monkeypatch): ...      # a raw TestClient
```

**After**

```python
# src/base/fixtures.py, imported by src/tests/conftest.py for every test
@pytest.fixture(scope="session")
def database(): ...
@pytest.fixture
def api(database, monkeypatch):
    ...
    yield TalkDeskApi(client)                  # a client that knows TalkDesk
```

**What it bought**

One home for setup that every test layer can use, outside the tests themselves.

**Tests that proved it was safe**

All 16 tests green before and after: [`framework-refactor-before.txt`](evidence/framework-refactor-before.txt),
[`framework-refactor-after.txt`](evidence/framework-refactor-after.txt), and green in the
pipeline ([run 37829745599](https://github.com/ztrudeau444/qe-capstone/actions/runs/37829745599)) at the same coverage, 87.90% line / 83.33% branch.

---

## R-07 — An API client in `pages/`

| | |
|---|---|
| **Date** | 2026-10-08 · commit `061db29` |
| **Principle** | DRY / DIP |
| **Trigger** | TalkDesk's URLs were written out 9 times across 3 test files. Moving one endpoint would have meant editing every test that used it. |

**Before**

```python
r = client.patch("/api/talks/1", json={"status": "accepted", "score": 9})
talks = client.get("/api/talks/search", params={"q": "flaky"}).json()
```

**After**

```python
r = api.review_talk(1, status="accepted", score=9)
talks = api.search_talks("flaky").json()
```

**What it bought**

URLs live in `pages/talkdesk_api.py` only, and the tests read as behaviour
rather than HTTP. Tests depend on `TalkDeskApi`, so the client behind it can
change without touching them.

**Tests that proved it was safe**

All 7 integration tests green before and after (same evidence as R-06).

---

## R-08 — Test data from an Object Mother in `utils/`

| | |
|---|---|
| **Date** | 2026-10-08 · commit `061db29` |
| **Principle** | DRY |
| **Trigger** | Each submission test wrote out a whole talk to change one field, which hid the field the test was actually about. |

**Before**

```python
client.post("/api/talks", json={
    "speaker_id": 999999, "title": "A valid title", "abstract": "", "track": "testing"})
```

**After**

```python
api.submit_talk(**valid_talk(speaker_id=999999))   # this test is about the speaker
```

**What it bought**

The one field that matters is the only one written in the test. A new rule
that needs a new field changes `valid_talk()` once.

**Tests that proved it was safe**

`test_valid_talk_is_created` and `test_unknown_speaker_is_rejected`: green
before and after (same evidence as R-06).

---

## Deferred

Things you saw and chose not to do. Week 4 Day 1 reads this list.

| # | What | Why deferred | Risk if never done |
|---|---|---|---|
| D-01 | The row-to-JSON block is copied five times (`list_talks`, `search_talks`, `get_talk`, `create_talk`, `patch_talk`), each copy slightly different | It runs only after the database is touched, and no test covers it yet. Changing untested code is a rewrite, not a refactor. Revisit in Week 2, once the integration tests for AC-01, 07, 08 and 09 exist | The endpoints drift apart: a field added to one reply is forgotten in the others |
| D-02 | Cryptic names in the database code (`r`, `sp`, `c`, `tid`, `trs`) | Same as D-01: no tests cover that code yet | Misreading the code during Week 3 performance tuning, the code most likely to be changed under pressure |

**Update 2026-10-08:** D-01 and D-02 are no longer blocked. The integration
tests (AC-01, 04, 07, 08, 09, 17 and the contract test) now run the database
code both items live in, so they can be done as refactors with a safety net.
