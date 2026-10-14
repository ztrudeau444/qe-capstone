# Non-Functional Test Strategy

Week 3. The tuning experiment at the bottom is the point of the week.

**What these numbers measure.** Every figure names its environment.
*Laptop*: Windows with Docker Desktop; k6, TalkDesk and PostgreSQL share one
machine. *Pipeline*: GitHub's `ubuntu-latest` runner, the same
`docker-compose.yml`, with k6 on the same runner. Neither is production
(reader §1: a load test on your own laptop measures your laptop).

## Quality attributes in scope

| Attribute | Why it matters here | Metric | Target | Source |
|---|---|---|---|---|
| Performance | Every visitor sees the list of talks first; if the list is slow, the whole app feels slow | p95 latency | ≤ 500 ms | k6 |
| Reliability | A fast error is not a success: the starter's script looked fast (p95 36 ms) while 29% of its requests failed | error rate | < 1% | k6 |
| Security | TalkDesk holds speakers' submissions and reviewers' decisions; SonarQube has already found hard-coded secrets (gap list #1, #11) | critical CVEs | 0 (the pipeline also blocks High: `max_high: 0`) | Snyk + ZAP |
| Accessibility | Speakers submit and reviewers review through web pages, which must work by keyboard and screen reader | Lighthouse score | ≥ 95 | Lighthouse |

Accessibility is measured on `/`, `/login` and `/submit` since the page template was fixed (gap list #3, PR #34); see Accessibility findings below.

## Workload model

*The model is the skill. Defend each number.*

| | Value | Why this number |
|---|---|---|
| Peak concurrent users | 50 | `quality/thresholds.yml` (the starter's value). TalkDesk has no real traffic data. 50 was enough to expose the list endpoint's tail on the laptop. |
| Ramp-up | 1 min | Lets the app and database warm up before the steady phase. |
| Steady-state duration | 3 min | The phase p95 should be read from. Limit: k6's summary also includes the ramps, and ramp traffic is light, so it flatters the median (this misled my first hypothesis; see below). |
| Ramp-down | 1 min | Currently the `load.js` fallback, not `thresholds.yml`: `ci.yml` does not pass `RAMP_DOWN` (reader §1.0 exercise, still open). |
| Scenario mix | Every visit lists talks; then 40% open one talk, 20% search, 10% submit a talk | A visitor sees the list first; most browse, few submit. Measured share of requests: list 58–60%, open 23–24%, search 11–12%, submit 6%. |
| Think time | 1–3 s, random, between visits | The starter's value. It makes this a closed model: 50 users cannot send much more than about 33 req/s however fast TalkDesk is. Seen in the experiment: p95 fell 98% but throughput rose only 25%. Reader §2.13 prefers an open model (`constant-arrival-rate`). |

**Where the numbers came from:** the starter's defaults (users, ramp, steady,
think time) and my own estimate for the mix. TalkDesk has no production
analytics, so these are defended guesses, not measurements of real users.

**Known limits of this workload:**

- **Warm cache.** The list returns the first 100 of about 50,000 talks
  (`ORDER BY id LIMIT 100`), and visitors only open talks they saw, so only
  those 100 are ever read.
- **The database grows** by about 500 talks per 5-minute run (the test's own
  submissions). This does not change the list (always the first 100), but it
  does grow the work search has to do.
- **The load generator and TalkDesk share a machine** in both environments.

## Baselines

| Metric | Week 1 | Week 2 | Week 3 first run (laptop · pipeline) | Week 3 after tuning (laptop · pipeline) |
|---|---|---|---|---|
| p95 latency | — | — | 1,060 ms · 28 ms | 21 ms · 26 ms |
| p99 latency | — | — | 1,320 ms · 41 ms | 38 ms · 51 ms |
| Error rate | — | — | 0% · 0% | 0% · 0% |
| Throughput | — | — | 27.9 · 33.7 req/s | 33.4 · 33.4 req/s |

Evidence, in `docs/evidence/week3/`: first run
[`load-talkdesk-full-local.txt`](evidence/week3/load-talkdesk-full-local.txt) ·
[`ci-loadtest-first.txt`](evidence/week3/ci-loadtest-first.txt); after tuning
[`tuning-after.txt`](evidence/week3/tuning-after.txt) ·
[`ci-loadtest-after-tuning.txt`](evidence/week3/ci-loadtest-after-tuning.txt).
The gate was also proven to fail in the pipeline (limit lowered to 10 ms on
purpose, run 37979508842):
[`ci-loadtest-gate-bites.txt`](evidence/week3/ci-loadtest-gate-bites.txt).

## Security findings

| ID | Severity | Finding | Decision | Owner | Review by |
|---|---|---|---|---|---|
| S-01 | Blocker (SonarQube) | Hard-coded database password in `app.py` | Fix: PR #23 | Zoe | Done 2026-10-09 |
| S-02 | Blocker (SonarQube) | Hard-coded reviewer login and demo token; the review endpoint never checks the token | Accept until real sign-in is built (gap list #1); accepted in SonarQube with that comment | Zoe | Week 4 |
| S-03 | 4 High, 3 Medium (Snyk) | starlette 0.41.3, via fastapi 0.115.6: ReDoS, SSRF, request smuggling, resource exhaustion and others | Fix: fastapi 0.143.0, starlette pinned at 1.8.0; Snyk 7 -> 0 (PR #31) | Zoe | Done 2026-10-13 |
| S-04 | ZAP: 4 FAIL, then WARNs | Missing security headers: 10020, 10021, 10038, 10055, 10063, 90004 (COEP, COOP, CORP), 10049 | Fix: headers on every reply, test-first (PR #33) | Zoe | Done 2026-10-13 |
| S-05 | ZAP WARN | 90005 Sec-Fetch-Dest missing: a header browsers send, not TalkDesk | False positive: IGNORE in `zap-rules.tsv`, with reason | Zoe | 2027-01-13 |
| S-06 | ZAP WARN | 10049 Non-Storable Content: the intended result of `Cache-Control: no-store` | Accept as INFO; a regression is caught by `test_security_headers.py` | Zoe | 2027-01-13 |
| S-07 | ZAP WARN | 10202 no anti-CSRF token on `/login` | Accept as INFO: TalkDesk sets no cookies, so a forged request carries no credentials. Revisit with real sign-in | Zoe | 2027-01-13 |
| S-08 | ZAP WARN | 10111 authentication request identified | Accept as INFO: ZAP noting a sign-in form, not a vulnerability | Zoe | 2027-01-13 |
| S-09 | High (code review) | Stored cross-site scripting on the home page | Fix: escaping, test-first (PR #35) | Zoe | Done 2026-10-13 |

**Gate result:** Snyk 0 Critical, 0 High; ZAP 0 FAIL, 0 WARN. The Security
stage is on and enforced (PR #33).

**What the scans cannot see.** ZAP runs the passive baseline scan: it looks,
it does not attack. Its SQL injection and XSS rules never run (gap list #15).
S-09 was found by reading the code, not by a tool.

*Every "Accept" also goes in `quality/thresholds.yml` under `security.accepted`
with the same expiry. Two places, because one is the record and the other is
the enforcement.* `security.accepted` is for Snyk CVEs, and none are accepted.
S-02 is enforced in SonarQube; S-05 to S-08 are ZAP rules, enforced by
`quality/security/zap-rules.tsv`, where each line carries its reason, owner
and review date.

## Accessibility findings

| Violation | Impact | Where | Fix | Status |
|---|---|---|---|---|
| Pages rendered only "Handler." | Nothing could be audited; blocked AC-13 and AC-14 | `/`, `/submit`, `/login` | Real template: page language, a title per page, a skip link, labelled navigation (PR #34) | Fixed |
| The tools could not test the real pages | No accessibility result was trustworthy | Pipeline | See gap list #19 (PR #36) | Fixed |

**Results** (run 38457918710, the first with the stage switched on):

| Tool | `/` | `/login` | `/submit` |
|---|---|---|---|
| axe (WCAG 2.1 A/AA) | 0 critical, 0 serious | 0 critical, 0 serious | not checked |
| pa11y (WCAG 2.0 AA) | 0 errors | 0 errors | 0 errors |
| Lighthouse score | 95 | 95 | not checked |

Lighthouse is exactly at the gate (95): it passes with no margin, and the
missing 5 points are not yet identified (gap list #20).

**Manual keyboard-only pass:** done on /login, 2026-10-14 (AC-13). Focus is
visible, the Tab order is logical, the skip link jumps past the menu, there are
no keyboard traps, and the sign-in form can be filled and submitted with the
keyboard alone. Submitting shows a raw 422 error page with no way back except
the browser's Back key (gap #17). Evidence:
`docs/evidence/week3/keyboard-pass-login.md`.

**Beyond the automated scan.** Roughly a third of WCAG *success criteria* are
machine-testable; Deque measured automated detection at 57% of *issue volume*.
The two are different measurements — Appendix C §C.7 sets them side by side. Record
what you checked by hand — keyboard-only navigation, focus order, one screen
reader pass.

---

## The tuning experiment

*One documented change, measured before and after. This is the Week 3 exit gate
and the strongest slide in your Week 4 defence.*

| | |
|---|---|
| **Hypothesis** | *"p95 is high because the list endpoint makes 101 database round trips per request"* (the planted N+1: one query for 100 talks, then one more per talk for its speaker). |
| **How you formed it** | A per-address breakdown of every request (k6 CSV output → `scripts/k6-by-endpoint.py`): the list's p95 was 1,110–1,218 ms, against about 100 ms for every other address, in three runs that agreed. The code's own comment confirms the N+1. My first guess, from the overall summary alone, was search; the breakdown corrected it. |
| **The one thing you changed** | Database queries per list request: 101 → 1, one `JOIN` fetching talks and speakers together (PR #29). Nothing else changed: same script, same 50 users, same 1m / 3m / 1m, same laptop, run back to back. |
| **Before** | p95 = 1,130 ms, error rate = 0%, throughput = 26.8 req/s (laptop; [`tuning-before.txt`](evidence/week3/tuning-before.txt)) |
| **After** | p95 = 21 ms, error rate = 0%, throughput = 33.4 req/s (laptop; [`tuning-after.txt`](evidence/week3/tuning-after.txt)) |
| **In the pipeline** | p95 28 ms → 26 ms: within run-to-run variation, so no measurable change on GitHub's runner |
| **Did it confirm the hypothesis?** |Yes, on my laptop, p95 dropped from 1,130 ms to 21 ms after reducing database queries from 101 to 1. In the pipeline, there was no measurable difference because database trips were already fast.|

**The delta and its cause, in one sentence:** Laptop p95 latency dropped from 1,130 ms to 21 ms because the JOIN fetched talks and speakers in one database query instead of 101.

**What you would try next.** Search is now the next bottleneck, with 39 ms p95, because it reads every title as the database grows. I would investigate search optimization and try an open workload model using constant-arrival-rate to test performance at a fixed request rate.