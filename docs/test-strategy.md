# Test Strategy

Week 2. Assessed at the Week 2 exit gate.

## Scope

| | |
|---|---|
| **System under test** | TalkDesk, the reference conference talk-submission system (Python 3.12 · FastAPI · PostgreSQL), in `src/talkdesk/` |
| **What is in scope** | TalkDesk's API: the submission rules, the review rules, listing, search, fetching a talk, and reviewer sign-in. What the database saves and returns. The shape of a talk reply (contract test). From Week 3: performance, security and accessibility. |
| **What is deliberately out of scope, and why** | **The web pages, for now.** They render only "Handler.", so there is nothing for a browser test to drive; E2E (AC-14) and the accessibility scan (AC-13) wait until they work. **TalkDesk's Java and .NET versions**: this project uses the Python one. **Fixing the planted defects**: most are Week 3 findings and are left in place on purpose (D-8 was fixed as the Week 1 TDD cycle, AC-15). |

## The layers

| Layer | What it covers here | Roughly how many | Runs in |
|---|---|---|---|
| Unit | The rules, decided in code before the database is touched: blank title, title length, track, score range, status, empty update, sign-in | 9 | Test stage |
| Integration | TalkDesk's API and the real database together: saving, listing, search, not-found, reviews, and the contract test | 7 | Test stage |
| E2E | A visitor browsing to a talk (AC-14). Blocked until the pages render | 0 now, 1–2 planned | Test stage |
| Smoke | The two or three checks that prove a deployment is alive | 0 until Week 4 | Smoke stage |

**Why this shape?** It is a pyramid in direction, with unit tests the largest layer and E2E the smallest, but the integration layer is nearly as big as the unit layer, and that is deliberate. TalkDesk is a thin API over a database: most of its behaviour lives in SQL (filtering, case-insensitive search, the defaults the database fills in, `UPDATE ... RETURNING`). A unit test replaces the database, so it cannot see any of that. Each criterion was placed at the lowest layer that could catch its failure (Week 1 Reader §3.8), and for this system that lowest layer is often integration. E2E stays at one or two journeys because each one is slow and only proves the wiring.

## Traceability

Every criterion in `acceptance-criteria.md` covered at the layer named there.

13 of 17 criteria have a passing test:

- **Unit:** AC-02, 03, 05, 06, 10, 15, 16
- **Integration:** AC-01, 04, 07, 08, 09, 17, plus the contract test

The 4 without a test, each with a reason:

- **AC-11** (errors expose no internals): a known gap, planted defect D-7, to be tested and triaged with the Week 3 security work.
- **AC-12** (p95 ≤ 500 ms under load): needs the Week 3 load stage.
- **AC-13** (accessible sign-in page) and **AC-14** (visitor browses to a talk): blocked by the pages rendering only "Handler."

## The Gherkin Decision

*Week 2 §2.9. The justification is assessed, not the decision. A well-reasoned
"no" scores higher than an unreasoned "yes".*

**The deciding question:** who, outside the engineering team, will read these
scenarios and be capable of telling you one is wrong?

| | |
|---|---|
| **Answer — a name, or "nobody"** | Nobody. The only other reader is my instructor, who reads the project to assess my engineering work, not to correct TalkDesk's requirements. |
| **Decision** | Do not adopt |

**Justification**

The one person outside me who reads this project is my instructor. They are capable of spotting a wrong scenario, but they read my work to grade it, not to tell me that TalkDesk should behave differently, so they are an engineering reader rather than the requirement owner Gherkin is for. Without someone outside engineering who will actually read and correct the scenarios, Gherkin would only translate my tests into a second language for an audience of myself. It would also add its costs: an extra hop when debugging (scenario, then step definition, then the failing code), a fragile link between sentences and functions that refactoring tools cannot follow, and two files to keep in sync. TalkDesk has no product owner, so those costs would buy nothing.

| | |
|---|---|
| **What it would buy us** | Scenarios a non-engineer could read and correct, and documentation that cannot drift from the behaviour because it runs. |
| **What it would cost us** | `pytest-bdd` and two new folders (`features/`, `steps/`), harder debugging and refactoring, and scenarios to keep in sync with the code, for no reader who would use them. |
| **What would change my mind** | A real requirement owner, such as a client, a conference organiser, or my instructor taking on a product-owner role, who agrees to read the scenarios and correct them. Or an audit or regulatory need to show, in business language, what the system guarantees. |

**If not adopting:** how do your acceptance criteria stay legible to anyone who
needs to read them?

They are already written in plain English, in the same Given / When / Then form Gherkin uses, in `docs/acceptance-criteria.md`, so anyone can read them without reading code. Each criterion names its test and test layer, and each test's description starts with its criterion number (for example "AC-17: a review is saved…"), so anyone can follow a criterion to the test that proves it, and back.

## Test data

| | |
|---|---|
| **Where it comes from** | TalkDesk's fixed seed, `db/02-seed.sql`: 200 speakers and 50,000 talks, the same on every run. Tests needing a new talk build one with `valid_talk()` in `src/utils/talk_data.py`, changing only the field the test is about. |
| **How it is isolated between runs** | Locally, the database lives in memory (`tmpfs` in `docker-compose.yml`), so every start begins from the same seed. In the pipeline, the database starts empty and `src/base/fixtures.py` loads the schema and seed. Tests that change data put it back in a `finally` block: a created talk is deleted, a changed review is restored. **Limit:** all tests share one database, so tests run in parallel could see each other's changes. They run one at a time today; if that changes, each test should get its own transaction. |
| **Anything sensitive, and how it is handled** | The seed data is invented, with no real people's details. The local database password (`qe`) is a disposable one that is already public in `docker-compose.yml`. Real credentials (`SONAR_TOKEN`, `SNYK_TOKEN`, the Render keys) live only in GitHub Secrets, never in the repository, and `verify-setup.sh` checks that `.env` is not tracked by Git. |

## Flaky test policy

| | |
|---|---|
| **How a flake is identified** | A test that fails and then passes on a re-run with no code change, or that passes on my laptop but fails in the pipeline. For E2E, the Week 2 rule applies: the suite must pass twice in a row. |
| **What happens to it** (quarantine? delete? fix within N days?) | Fix within 2 working days. Until then it is marked (`pytest.mark.xfail(strict=False, reason=...)` with the date), so it keeps running and reporting but cannot block a merge. After 2 days it is either fixed, or deleted with the missing check recorded on the gap list. A flaky test is never simply re-run until it passes. |
| **Who owns that decision** | Me (Zoe Trudeau), as the sole owner of this test suite. |