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
| 25 | **Speakers must know their Speaker ID number** to submit a talk. Real speakers don't know it; the form should ask for name and email instead. Needs an API change, since `NewTalk` takes `speaker_id`. | Using the new /submit form (gap #18) | Low | M | Zoe | Week 4 | ☐ |
| 2 | **Error replies expose internals** (D-7): a bad talk ID returns the exception, message and full traceback. | `acceptance-criteria.md`: AC-11 has no test | High | S | Zoe | Week 3 (security) | ☐ |
| 3 | **The web pages rendered only "Handler."** A planted defect (confirmed by the instructor, 2026-10-09): the shared page template had no {title} or {body} placeholders. Fixed test-first; unblocks AC-13 and AC-14. | Ledger: E2E rows unticked | High | S | Zoe | 2026-10-13 | ☒ PR #34 |
| 4 | **Snyk did not scan TalkDesk's dependencies.** The pipeline ran `snyk test` at the repository root, found no manifest and failed (SNYK-CLI-0008); now pointed at `src/talkdesk/requirements.txt`. The Snyk GitHub app's own check still does not watch that file. | Pipeline: Snyk check | Med | S | Zoe | 2026-10-13 | ☒ PR #32 (pipeline) |
| 5 | **No load test yet** for the list endpoint, where the planted N+1 lives. | `acceptance-criteria.md`: AC-12 has no test | Med | M | Zoe | Week 3 | ☐ |
| 6 | **SonarQube has never analysed the project.** The scanner was never installed (fixed in PR #20), and the maintainability gate is still off. Switched on 2026-10-09; the first analysis found 2 blocker vulnerabilities (see #11 and #1). | Pipeline: skipped step | Med | S | Zoe | 2026-10-09 | ☒ PR #20, #22 |
| 7 | **The framework's dependency rule is checked by hand only** (a `grep`, in `framework-architecture.md`). Nothing fails the build if it is broken. | `framework-architecture.md` | Low | S | Zoe | Week 4 | ☐ |
| 8 | **All tests share one database.** Run in parallel, they could see each other's changes. | `test-strategy.md` | Low | M | Zoe | Only if tests go parallel | ☐ |
| 9 | **`analyze.sh` still claims the setup step installs sonar-scanner.** The pipeline no longer uses it for Python, but the comment misleads. | Pipeline | Low | S | Zoe | Week 4 | ☐ |
| 10 | **Coverage counted the test files**, inflating the gate's number (86% vs an honest 76%). | Found while testing | Med | S | Zoe | 2026-10-08 | ☒ PR #11, #15 |
| 11 | **Hard-coded database password in `app.py`**: the fallback `DB_URL` had a username and password in the code. SonarQube blocker. | SonarQube, first analysis | High | S | Zoe | 2026-10-09 | ☒ PR #23 |
| 12 | **Vulnerable dependencies.** SonarQube Cloud reported 11 dependency risks; once Snyk scanned TalkDesk it found 7 (4 High, 3 Medium), all in starlette 0.41.3 via fastapi 0.115.6. fastapi upgraded to 0.143.0 and starlette pinned at 1.8.0: Snyk 7 -> 0, all tests pass. SonarQube's own count not yet re-checked. | SonarQube, then Snyk | High | S | Zoe | 2026-10-13 | ☒ PR #31 (Snyk 0); SonarQube re-check ☐ |
| 13 | **ZAP never read its rules file.** `rules_file_name` was accepted, but no `-c` reached ZAP, so every rule was ignored (FAIL rules came out as WARN). Passed through `cmd_options` instead. | Pipeline: ZAP command line, run 38436325721 | High | S | Zoe | 2026-10-13 | ☒ PR #33 |
| 14 | **Security headers missing** (clickjacking, nosniff, CSP, permissions policy, COEP/COOP/CORP, no-store). Added to every reply, test-first. | ZAP baseline | Med | S | Zoe | 2026-10-13 | ☒ PR #33 |
| 15 | **ZAP's SQL injection and XSS rules never run.** 40012, 40014 and 40018 are active-scan rules; the pipeline runs the passive baseline scan, so those FAIL lines give false comfort. Needs an active scan against a disposable environment. | `zap-rules.tsv` vs the scan type | High | M | Zoe | Week 4 | ☐ |
| 16 | **Stored cross-site scripting on the home page.** Title, speaker name, track and status were pasted into the HTML unescaped. Escaped, test-first. Found by reading the code; the baseline scan cannot find it (see #15). | Code review | High | S | Zoe | 2026-10-13 | ☒ PR #35 |
| 17 | **The sign-in form cannot sign in.** It posts form data; `/api/login` accepts only JSON, so the browser gets a 422 (seen by ZAP, rule 10111). Fixed: the form now posts to a new POST /login, which answers with a page. Real sign-in is still #1. | ZAP baseline | Med | M | Zoe | 2026-10-14 | ☒ PR #42 |
| 18 | **The submit page has no form**: `/submit` still shows "Handler." inside the template, so speakers cannot submit through the site. The second half of the planted page defect. Fixed: `/submit` now shows a labelled form (track choices come from TRACKS), and POST /submit saves through `create_talk()`, the same rules as the API, answering with a "Thanks" page or a readable error with a way back. | Code, while fixing #3 | Med | M | Zoe | 2026-10-14 | ☒ PR #44 |
| 19 | **The accessibility stage could not have passed.** `check-a11y.py` had a SyntaxError; pa11y checked `/items`, which TalkDesk does not have; axe and Lighthouse checked only the home page; axe's ChromeDriver did not match the runner's Chrome; a comma-separated list was scanned as one address. All fixed before the stage counted. | Pipeline, before enabling | High | S | Zoe | 2026-10-13 | ☒ PR #36 |
| 20 | **Lighthouse accessibility is exactly at the gate** (95 on `/` and `/login`): no margin, and the 5 points lost are not yet identified. | Pipeline, run 38457918710 | Low | S | Zoe | Week 4 | ☐ |
| 21 | **New talks never appear in the list.** It returns the first 100 talks by id, so newer submissions are invisible. Fixed: the list now returns the newest 100 (descending id, still the indexed key; the load-test p95 gate stayed green). AC-07 changed from "ascending ID order" to newest first, since the old wording itself caused this gap. | Load testing | Med | M | Zoe | 2026-10-14 | ☒ PR #48 |
| 22 | **Search is the next bottleneck** (p95 39 ms after the N+1 fix): it reads every title, and the table grows with every submission. | Tuning experiment | Low | M | Zoe | Week 4 | ☐ |
| 23 | **`ramp_down` in `thresholds.yml` is read by nothing**: `ci.yml` does not pass `RAMP_DOWN` (reader §1.0 exercise). | Reader §1.0 | Low | S | Zoe | Week 3 | ☐ |
| 24 | **Small code issues found in passing:** in `check-a11y.py`, `... + len(nodes) or 1` groups the `or` wrongly (miscount in a rare case); starlette warns that its test client's use of `httpx` is deprecated. Fixed: the `or 1` now applies to each violation's nodes, so two node-less critical violations count as 2 and fail a limit of 1. The httpx warning moved to #25. | Code reading, test warnings | Low | S | Zoe | 2026-10-14 | ☒ PR #46 |
| 26 | **Only the newest 100 talks can be listed.** Older talks are reachable only by search or by id; there is no "next page". Found while fixing #21. | Code, while fixing #21 | Low | M | Zoe | Week 4 | ☐ |

## Accepted, not closed

Anything you consciously decide not to fix. This is a legitimate outcome — an
undocumented one is not.

| Gap | Why accepted | What would change the decision |
|---|---|---|
| The planted defects D-1 to D-6 (N+1 query, unindexed search, no login rate limit, unlabelled form field, low contrast, missing security headers) | They are the Week 3 exercises: fixing them now would remove what Week 3 is meant to find. D-8 and D-9 were closed in Week 1. | Week 3 itself: each one is triaged and fixed or accepted then. |
| Names in `home()` (`trs`, `t`) not refactored | No test covers the web pages, so renaming there is a change without a safety net (see R-10). | The pages rendering, and a test covering `home()`. |

---

**The one you have been avoiding.** The web interface. Every test so far goes around it, through the API, because the pages do not work. TalkDesk's real users would only ever see the pages.