# Gap List

Week 4, Day 1. You work from this for two days.

**Ranked by risk, not effort.** The honesty of this document is assessed — a
short list nobody believes scores worse than a long one that is accurate.

*Started early, on 2026-10-08 (Week 2), from findings made while building, so
they are not lost before Week 4. Re-ranked on Week 4 Day 1.*

## Sources

Work through all four before ranking:

1. Carry-Forward Ledger — every unticked box
2. `acceptance-criteria.md` — every criterion with no test
3. `refactor-log.md` — every deferred item
4. Last pipeline run — every amber or skipped stage

## The list

| # | Gap | Source | Risk if shipped | Effort | Owner | Target day | Done |
|---|---|---|---|---|---|---|---|
| 1 | **Anyone can review a talk.** `PATCH /api/talks/{id}` never checks for a sign-in token, so anyone can accept, reject or score any talk. Not one of the nine planted defects; found while writing AC-17. Related: the login accepts a hard-coded password (`reviewer`) and hands out a fixed demo token; SonarQube flagged the token, and the issue was accepted on 2026-10-09 with a comment pointing to this gap. | Found while testing (AC-17) | High | M | Zoe | Week 3 (security) | ☐ |
| 2 | **Error replies expose internals** (D-7): a bad talk ID returns the exception, message and full traceback. | `acceptance-criteria.md`: AC-11 has no test | High | S | Zoe | Week 3 (security) | ☐ |
| 3 | **The web pages render only "Handler."** No page works for a user, so E2E (AC-14) and accessibility (AC-13) cannot be tested. TalkDesk's own `test_submit_page_renders` fails on it too. | Ledger: E2E rows unticked | High | ? (needs instructor) | Instructor / Zoe | Ask now; Week 2 | ☐ |
| 4 | **Snyk does not scan TalkDesk's dependencies.** Its green check says "no manifest changes in 3 projects"; `src/talkdesk/requirements.txt` is not one of them. | Pipeline: Snyk check | Med | S | Zoe | Week 3 | ☐ |
| 5 | **No load test yet** for the list endpoint, where the planted N+1 lives. | `acceptance-criteria.md`: AC-12 has no test | Med | M | Zoe | Week 3 | ☐ |
| 6 | **SonarQube has never analysed the project.** The scanner was never installed (fixed in PR #20), and the maintainability gate is still off. Switched on 2026-10-09; the first analysis found 2 blocker vulnerabilities (see #11 and #1). | Pipeline: skipped step | Med | S | Zoe | 2026-10-09 | ☒ PR #20, #22 |
| 7 | **The framework's dependency rule is checked by hand only** (a `grep`, in `framework-architecture.md`). Nothing fails the build if it is broken. | `framework-architecture.md` | Low | S | Zoe | Week 4 | ☐ |
| 8 | **All tests share one database.** Run in parallel, they could see each other's changes. | `test-strategy.md` | Low | M | Zoe | Only if tests go parallel | ☐ |
| 9 | **`analyze.sh` still claims the setup step installs sonar-scanner.** The pipeline no longer uses it for Python, but the comment misleads. | Pipeline | Low | S | Zoe | Week 4 | ☐ |
| 10 | **Coverage counted the test files**, inflating the gate's number (86% vs an honest 76%). | Found while testing | Med | S | Zoe | 2026-10-08 | ☒ PR #11, #15 |
| 11 | **Hard-coded database password in `app.py`**: the fallback `DB_URL` had a username and password in the code. SonarQube blocker. | SonarQube, first analysis | High | S | Zoe | 2026-10-09 | ☒ PR #23 |
| 12 | **11 dependency risks** reported by SonarQube Cloud on `main` (rated E; no gate condition on them, so the pipeline stays green). Not yet reviewed. Snyk is not catching these (see #4). | SonarQube, first analysis | High | ? | Zoe | Week 3 (security) | ☐ |

## Accepted, not closed

Anything you consciously decide not to fix. This is a legitimate outcome — an
undocumented one is not.

| Gap | Why accepted | What would change the decision |
|---|---|---|
| The planted defects D-1 to D-6 (N+1 query, unindexed search, no login rate limit, unlabelled form field, low contrast, missing security headers) | They are the Week 3 exercises: fixing them now would remove what Week 3 is meant to find. D-8 and D-9 were closed in Week 1. | Week 3 itself: each one is triaged and fixed or accepted then. |
| Names in `home()` (`trs`, `t`) not refactored | No test covers the web pages, so renaming there is a change without a safety net (see R-10). | The pages rendering, and a test covering `home()`. |

---

**The one you have been avoiding.** The web interface. Every test so far goes around it, through the API, because the pages do not work. TalkDesk's real users would only ever see the pages.