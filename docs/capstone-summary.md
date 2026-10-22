# TalkDesk capstone — summary

*Zoe Trudeau · QE capstone · updated 2026-10-22*

**What I built:** a quality pipeline for TalkDesk (a conference talk-submission app: Python, FastAPI, PostgreSQL). Every change goes through **8 stages** — Build → Test → Analyze → LoadTest → Security → Accessibility → Deploy → Smoke — and **nothing reaches `main` unless every gate is green**.

## Where it stands

| Measure | Result | Gate |
|---|---|---|
| Tests | 47 unit, 8 integration, 1 end-to-end (real browser) | all must pass |
| Coverage (Week 3 ledger) | 96% lines, 91% branches | ≥ 80% / ≥ 60% |
| Speed under load (CI) | p95 30 ms, 0% errors | ≤ 500 ms, < 1% |
| Capacity (stress test) | levels off at ~88 requests/s; 0 errors even at 400 users | — |
| Security | 0 critical / 0 high CVEs | 0 high |
| Accessibility | Lighthouse 95–96 on all 4 pages; axe and pa11y clean | ≥ 95 |
| Requirements | 16 of 18 with a test; the other 2 (AC-12, AC-13) enforced by pipeline gates | — |

## Found it → proved it → fixed it

1. **Slow talk list (N+1 queries).** The list made 101 database trips per page. I measured it, changed one thing (a JOIN), and measured again: p95 went from **1,130 ms to 21 ms** on my laptop. (`docs/NFT-Strategy.md`, dashboards in `docs/evidence/week3/`)
2. **Anyone could review a talk (gap #1).** Tests showed a stranger's review got through; I added a sign-in check with fresh random tokens, and a stranger now gets 401. SonarQube then caught a password I had written into my own test helper — I fixed it rather than override the gate. (PRs #63–#65, AC-18)
3. **Speaker emails were public (gap #29).** Spotted while building the talk page. I changed the API **contract test first** (red), then the code (green), so the change was deliberate and recorded. (PRs #58–#60)
4. **Errors leaked internals (gap #2).** Error replies showed a full stack trace (4.5 KB). Now visitors get a short message with a reference number, and the details go only to the server log. (PRs #53–#55, AC-11)
5. **The "known gap" since Week 2 (AC-14).** Clicking a talk showed raw JSON. I wrote a real-browser test (Playwright), built the talk page, and when the test first failed in CI (no browser there), I split the pipeline so E2E runs where the site is running. (PR #57)
6. **A tool failure, not a code failure.** SonarQube rejected a docs-only change three times. Its own error report showed the project had become private, and the free plan only analyses public projects. I fixed the setting without bypassing the gate. (PR #56)
7. **Testing my own quality gate (gap #31).** A pull request merged while three stages were still running. GitHub's settings showed that only 3 of my 8 stages were required to pass. I made the final "Quality summary" check required too, then proved it: an immediate merge was refused until every stage passed. (PR #67)

## Honestly still open

- Sign-in is still a demo: shared password, tokens kept in memory (gap #30).
- A long soak run showed p95 of 797 ms — above the gate the 5-minute load test passes; not yet investigated.
- Lighthouse scores sit right at the 95 gate (gap #20).
- Search slows as the data grows (gap #22); no active ZAP scan yet (gap #15).

Full list: `docs/gap-list.md`.

## In my words

- **What surprised me most:** How often the problem was not in TalkDesk's code but in the tools and settings around it: a quality tool set to private, a browser missing in CI, and a merge rule that only checked 3 of 8 stages. The pipeline is a product too, and it needs testing like any other. I was also surprised how much measuring matters: one change (a JOIN) made the talk list about 50 times faster, and I would have guessed the wrong cause without the numbers.
- **What I would do next with another week:** Real sign-in (gap #30), because it is now the biggest remaining risk: proper accounts, stored password hashes and tokens that expire. Then find out why the long soak run slowed to a p95 of 797 ms when the 5-minute load test stays at 30 ms, and add an active security scan (gap #15). I would take them in that order, highest risk first.
