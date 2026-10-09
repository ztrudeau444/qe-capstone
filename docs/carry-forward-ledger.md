<!-- Learner's copy, filled in at the end of each week. Originally generated
     from the canonical Carry-Forward Ledger in the learner materials. -->

# What this is

One page you update at the end of every week. It records what you now have, so the program accumulates visibly rather than feeling like four separate topics.

Two things make it worth taking seriously.

**It is how the exit gates are verified.** Your instructor walks this with you at the end of each week. An unticked box is not a failure — it is a known gap you carry forward deliberately rather than discover in Week 4.

**The trend table at the bottom becomes your capstone metrics report.** Fill it in weekly and you will have written your final deliverable without noticing. Leave it until Week 4 and you will have no trend to report, because the readings will not exist.

---

# Identification

| | |
|---|---|
| **Learner** | Zoe Trudeau |
| **System Under Test** | TalkDesk (reference system, Python) |
| **Repository URL** | https://github.com/ztrudeau444/qe-capstone |
| **Language / stack** | Python 3.12 · FastAPI · PostgreSQL |
| **Instructor** | |
| **Cohort start date** | |

> The System Under Test and the repository do not change for four weeks. If either changes, tell your instructor — it invalidates the trend.

---

# Week 1 — Make it testable

**Block produced:** a testable system with criteria you can test against.

| ☐ | Item | Record |
|---|---|---|
| ☒ | Repository on `main`, unit suite green | Commits: 27 |
| ☒ | Container builds and runs | Build time: 11 s |
| ☒ | `docs/acceptance-criteria.md` written | Criteria: 15 (F: 12 NF: 3) |
| ☒ | One strict TDD cycle, three separate commits | Commit SHAs: `05fe645` (red), `9631f9b` (green), `ab25830` (refactor) |
| ☒ | Unit suite covering core logic | Tests: 8 Runtime: 1.4 s |
| ☒ | **Coverage baseline recorded** | 90 % (TalkDesk's shipped suite) |
| ☒ | `docs/refactor-log.md` | Refactors: 5 **(gate 2)** |
| ☒ | Traceability template filled, gaps visible | Criteria with a test: 6 of 15 |

**Carried into Week 2 (anything unticked, and why):**

Coverage 55% line / 43% branch, below the gates enforced from Week 2; integration tests for AC-01, 04, 07, 08, 09 will close it. Invalid-status rule has no test (found during R-05). Refactors D-01 and D-02 deferred until integration tests exist.

Web pages show only "Handler.", so AC-13 and AC-14 are blocked (TalkDesk's own `test_submit_page_renders` also fails). Snyk does not scan `src/talkdesk/requirements.txt`.

**Instructor verification** — date: `__________` initials: `______`

---

# Week 2 — Make it verifiable

**Block produced:** a pipeline that proves functional correctness.

| ☐ | Item | Record |
|---|---|---|
| ☒ | Framework layers in place | `base` `pages` `utils` `config` `tests` |
| ☒ | Integration tests written | Count: 7 Types: API + database (6), contract (1) |
| ☐ | E2E tests derived from acceptance criteria | Count: ______ |
| ☐ | E2E suite passes **twice consecutively** | Run 1: ____ Run 2: ____ |
| ☒ | Static analysis connected | **Maintainability grade: A** (gate A) · first full analysis 2026-10-09, [run 37945043114](https://github.com/ztrudeau444/qe-capstone/actions/runs/37945043114) |
| ☐ | CI pipeline green on push | Green runs: ______ |
| ☒ | **Coverage gate enforced at 80%** | 87.90 % (line; branch 83.33 %) |
| ☒ | Gate proven to work (a run that failed it) | Yes: run 37817280239, see docs/evidence/ |
| ☒ | `docs/framework-architecture.md` | Committed |
| ☒ | **Gherkin decision recorded, with justification** | Adopt ☐ / Decline ☒ — audience named: nobody (see docs/test-strategy.md) |

**Carried into Week 3:**

`________________________________________________________________`

`________________________________________________________________`

**Instructor verification** — date: `__________` initials: `______`

---

# Week 3 — Make it trustworthy

**Block produced:** enforced gates across every quality attribute.

| ☐ | Item | Record |
|---|---|---|
| ☐ | Load stage in pipeline, threshold enforced | **p95: ______ ms** (gate ≤ 500) |
| ☐ | Error rate under load | ______ % (gate < 1) |
| ☐ | Knee point identified | ______ virtual users |
| ☐ | Security stage, gate enforced | **Critical CVEs: ____ · High CVEs: ____** (gate 0 and 0) |
| ☐ | Findings triaged with reasoning | Total: ____ Real: ____ Accepted: ____ |
| ☐ | Accessibility stage, gate enforced | **Score: ____ · critical: ____ · serious: ____** (gate ≥ 95, 0, 0) |
| ☐ | Manual keyboard-only pass done | Issues found: ______ |
| ☐ | **Tuning experiment documented** | See below |
| ☐ | Dashboard showing p50/p95/p99 + throughput | Link: ______________ |
| ☐ | `docs/NFT-Strategy.md` | Committed |

**The tuning experiment** — one variable only:

| | |
|---|---|
| What I changed | |
| p95 before | ______ ms |
| p95 after | ______ ms |
| Why it worked | |

**Carried into Week 4:**

`________________________________________________________________`

`________________________________________________________________`

**Instructor verification** — date: `__________` initials: `______`

---

# Week 4 — Assemble and defend

**Block produced:** evidence, and the ability to argue from it.

| ☐ | Item | Record |
|---|---|---|
| ☐ | `docs/gap-list.md` — ranked by risk | Items: ____ Closed: ____ Accepted: ____ |
| ☐ | Deploy stage added, pipeline-triggered | |
| ☐ | Smoke stage added, inside the pipeline's 5-minute timeout | Runtime: ______ s |
| ☐ | Smoke proven to catch a broken deployment | Yes / No |
| ☐ | **Full pipeline green from one commit** | All 8 stages · run: ______________ |
| ☐ | 100% of functional criteria covered | ____ of ____ |
| ☐ | `docs/metrics-report.md` with trend | |
| ☐ | At least one regression explained honestly | |
| ☐ | Defence delivered and questioned | Date: ______________ |

**Instructor verification** — date: `__________` initials: `______`

---

# Four-week trend

**This table is your capstone metrics report.** Fill one column per week.

| Metric | Week 1 | Week 2 | Week 3 | Week 4 | Gate |
|---|---|---|---|---|---|
| Line coverage % | 55 | 88 |  |  | ≥ 80 |
| **Branch coverage %** | 43 | 83 |  |  | **≥ 60** |
| Maintainability grade | — | | | | A |
| Unit tests | 8 | 9 |  |  | — |
| Integration tests | — | 7 |  |  | — |
| E2E tests | — | 0 |  |  | — |
| Suite runtime (s) | 1.4 | 0.9 |  |  | — |
| p95 latency (ms) | — | — | | | ≤ 500 |
| Error rate under load % | — | — | | | < 1 |
| Critical CVEs | — | — | | | 0 |
| **High CVEs** | — | — | | | **0** — this is the one `ci.yml` gates on |
| Accessibility score | — | — | | | ≥ 95 |
| Criteria covered | 6/15 | 13/17 | ____/____ | ____/____ | 100% F |
| Pipeline stages green | — | ____/3 | ____/6 | ____/8 | 8 |

---

# Closing reflection

Complete in Week 4, before your defence. These are the questions you will be asked.

**Which of your findings could only have been found by the layer that found it?**

`________________________________________________________________`

`________________________________________________________________`

**Which metric moved in the wrong direction, and why?**

`________________________________________________________________`

**What remains wrong with your system that you are choosing to accept?**

`________________________________________________________________`

**What would you do differently if you started again on Monday?**

`________________________________________________________________`

`________________________________________________________________`