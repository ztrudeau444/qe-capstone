# Framework Architecture

Week 2. This becomes the architecture slide in your Week 4 defence, so draw it
once and keep it current.

## Layers

```
src/
 ├── base/      fixtures.py: the shared test setup. `database` (TalkDesk's
 │              schema and seed, loaded if missing) and `api` (TalkDesk's real
 │              API, pointed at that database).
 ├── pages/     talkdesk_api.py: TalkDeskApi, an API client. The only place
 │              that knows TalkDesk's URLs. Page objects for the web pages go
 │              here too, once the pages render (see "What this design makes hard").
 ├── utils/     talk_data.py: valid_talk(), test data that passes every rule.
 │              db.py: count talks, read or reset a review, delete a talk,
 │              straight from the database.
 ├── config/    settings.py: where the database is, read from the environment.
 │              Names of things, never real secrets.
 ├── tests/     one folder per layer: unit/ (9), integration/ (7, including the
 │              contract test), e2e/ and smoke/ (empty until the pages work).
 └── talkdesk/  the System Under Test. Not part of the framework: it imports
                nothing from it.
```

## The dependency rule

Dependencies point one way, towards the system under test:

```
tests  →  base, pages, utils, config  →  talkdesk
```

- `tests/` may import any framework layer. Nothing imports `tests/`.
- `base/` wires things together, so it imports `config/`, `pages/` and `talkdesk/`.
- `pages/` imports nothing. It is handed a client and only knows URLs.
- `utils/` imports only the database driver.
- `config/` imports only `os`.
- `talkdesk/` imports nothing from the framework. The system must not know it is being tested.

**How I would notice if someone broke it:** honestly, nothing automatic yet.
The check is manual. This should print nothing:

```bash
grep -rnE "^(from|import) (tests|base|pages|utils|config)" src/talkdesk src/pages src/utils src/config
```

An import-linter rule in the pipeline would make it automatic; that is a
reasonable Week 4 gap-list item.

## Patterns used

| Pattern | Where | Why here rather than the simpler thing |
|---|---|---|
| API client (the Page Object idea applied to an API, Appendix E §E.6.1) | `pages/talkdesk_api.py` | The simpler thing was calling `client.post("/api/talks", ...)` in each test. TalkDesk's URLs were written out 9 times across 3 test files, so moving an endpoint meant editing every test. Now it is one line in one file, and tests read as behaviour: `api.review_talk(1, status="accepted", score=9)`. |
| Object Mother (Appendix E §E.3.5) | `utils/talk_data.py` | Every submission test needed a valid talk that differed in one field. Writing the whole dictionary each time hid which field the test was about. `valid_talk(speaker_id=999999)` shows it. A full Builder would be more machinery than a flat dictionary needs. |
| Fixtures as dependency injection | `base/fixtures.py` | Tests ask for `api` and `database` by name instead of building them. Setup lives in one place, so no test can forget to point TalkDesk at the right database. |
| **Not used:** Driver Factory (workbook §3 offers it as one option) | — | There is one kind of client and no browsers yet, so a factory would choose between one option. The workbook's other option, a shared fixture, is what was built. A factory earns its place when E2E adds browsers. |

## What this design makes hard

- **Finding where things come from.** `api` appears as a test parameter with
  no import; pytest finds it through `src/tests/conftest.py`. Someone new has
  to know to look there.
- **Seeing the URL.** Reading a test, you see `api.get_talk(1)`, not
  `GET /api/talks/1`. To see the request, you open `pages/`.
- **Changing the database schema.** `utils/db.py` reads columns (`status`,
  `score`) directly, so a schema change breaks the helpers as well as TalkDesk.
- **Testing the real server.** `api` drives TalkDesk in-process through
  FastAPI's TestClient. That is fast and needs no running container, but it
  never exercises uvicorn, the network or the Docker wiring. Those are only
  covered once E2E and smoke tests run against the container.
- **E2E is blocked, not designed.** TalkDesk's pages render only "Handler.",
  so `pages/` holds an API client and no page objects yet.

## Traceability to Week 1

- **SRP (R-04, R-05).** In Week 1 the submission and review rules were split
  out of the functions that write to the database, so each part has one reason
  to change. The layers apply the same argument to the tests: `pages/` changes
  when URLs change, `utils/` when test data or the schema changes, `base/` when
  setup changes, and a test only when the behaviour it checks changes.
- **DRY (R-02).** The shared `no_database` fixture replaced setup copied into
  each unit test. `base/` is that idea grown into a layer: `database` and `api`
  are defined once for every integration test.
- **DIP.** Tests depend on `TalkDeskApi`, not on how requests are made. The
  fixture decides which client sits behind it: TestClient today, a real HTTP
  client pointed at a deployed TalkDesk for smoke tests later, without
  changing the tests.
