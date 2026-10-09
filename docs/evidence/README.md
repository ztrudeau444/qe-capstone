# Evidence

Proof for exit gates and project tasks. GitHub deletes Actions logs after
90 days, so the gate's own output is copied here alongside each run link.

## Week 2: the coverage gate

### Switched on (workbook 4b)

| Flag | Date | Commit | Run | Result |
|---|---|---|---|---|
| `coverage.enabled` | 2026-10-08 | `d4918e5` | [run 37814786461](https://github.com/ztrudeau444/qe-capstone/actions/runs/37814786461) | Green, 87.90% line / 83.33% branch (gate ≥ 80 / ≥ 60) |

Gate output: [`coverage-gate-enabled.txt`](coverage-gate-enabled.txt)

### Proven to bite (workbook 4b, "Make a gate bite")

The integration tests were skipped on purpose. Every test that still ran
passed, so 2 · Test stayed green, but 3 · Analyze went red because too
little of TalkDesk's code was being tested. A revert restored the tests.

| Step | Commit | Run | 2 · Test | 3 · Analyze |
|---|---|---|---|---|
| Break: integration tests skipped | `97ebd4f` | [run 37817280239](https://github.com/ztrudeau444/qe-capstone/actions/runs/37817280239) | Green | **Red**: 54.84% line (gate 80), 40.00% branch (gate 60) |
| Restore: the skip reverted | `a46f6ef` | [run 37817813666](https://github.com/ztrudeau444/qe-capstone/actions/runs/37817813666) | Green | Green: 87.90% line, 83.33% branch |

Both commits are in [pull request #13](https://github.com/ztrudeau444/qe-capstone/pull/13).

- Gate output, failing: [`coverage-gate-failed.txt`](coverage-gate-failed.txt) · full log: [`coverage-gate-failed-full.log`](coverage-gate-failed-full.log)
- Gate output, restored: [`coverage-gate-restored.txt`](coverage-gate-restored.txt)
- Pull request #13, merged after the restore: [`pr-red-then-green.png`](pr-red-then-green.png)
- Its commits, red then green: [`pr-red-then-green-commits.png`](pr-red-then-green-commits.png)

**What the log said, in my words:** When I skipped the integration tests, coverage dropped to 54.84% for lines and 40% for branches. The Analyze stage failed because both were below the required 80% and 60%.

**What this proves:** Passing tests does not guarantee the quality gate passes. The gate also checks coverage, even when all executed tests pass.

## Week 2: framework layers (Stage 3)

The tests were restructured into `base/`, `pages/`, `utils/` and `config/`
(commit `061db29`). Same 16 tests, same results:

- Before: [`framework-refactor-before.txt`](framework-refactor-before.txt) · After: [`framework-refactor-after.txt`](framework-refactor-after.txt)
- Pipeline: [run 37829745599](https://github.com/ztrudeau444/qe-capstone/actions/runs/37829745599), Analyze unchanged at 87.90% line / 83.33% branch.
- Coverage now measures `src/talkdesk` only (commit `54d09ba`), so the new
  framework code, which the tests use and so would be 100% covered, cannot
  inflate the gate's number.

## Week 2: deferred refactors D-01 and D-02

- R-09 (D-01, shared reply fields) and R-10 (D-02, clear names): 16 tests green
  before and after: [`deferred-refactors-before.txt`](deferred-refactors-before.txt)
  · [`deferred-refactors-after.txt`](deferred-refactors-after.txt).
- **A note on commit `4f7fc30`.** Its message says "refactor log R-09, R-10; D-01
  and D-02 done", but the refactors had not run yet: a helper script failed to
  paste, and the commit captured only two test-output files. The refactors are the
  later commits `refactor(R-09)` and `refactor(R-10)`. The misleading message was
  left in place rather than rewriting history that had already been pushed.

## Week 2: Maintainability gate (SonarQube Cloud)

Switched on in `quality/thresholds.yml` (`maintainability.enabled: true`), on a
different day from the coverage gate, as the workbook asks. The rule: grade A,
no new code smells. The first full analysis of `main` failed SonarQube's
quality gate, not on maintainability but on **security**.

| Step | PR / commit | Run | 3 · Analyze | SonarQube |
|---|---|---|---|---|
| Gate switched on | [PR #22](https://github.com/ztrudeau444/qe-capstone/pull/22) | | Green | Passed: PR had 0 new lines of code |
| First analysis of `main` | merge `b77d541` | [run 37930258190](https://github.com/ztrudeau444/qe-capstone/actions/runs/37930258190) | **Red** | **Failed**: Security E, 2 blocker vulnerabilities (hard-coded secrets). Maintainability A, Reliability A |
| Fix 1: database password removed from `app.py` | [PR #23](https://github.com/ztrudeau444/qe-capstone/pull/23), first push | | **Red** | **Failed**: new-code coverage 66.7% (gate 80%); the new safety check had no test |
| Fix 1, with a test for the safety check | [PR #23](https://github.com/ztrudeau444/qe-capstone/pull/23), second push | | Green | Passed: new-code coverage 100% |
| Fix 2: demo token triaged as **Accepted** in SonarQube, with a comment linking gap list #1 (real sign-in, Week 3) | no code change | | | |
| Re-run of `main` | merge `9b38b2c` | [run 37945043114](https://github.com/ztrudeau444/qe-capstone/actions/runs/37945043114) | Green | **Passed**. Maintainability A, coverage 88.0% |

- PR #22 summary: [`sonar-pr22.png`](sonar-pr22.png)
- First `main` analysis, failed: [`sonar-main-first-run.png`](sonar-main-first-run.png) · overall grades: [`sonar-overall.png`](sonar-overall.png) · the two blockers: [`sonar-security-issues.png`](sonar-security-issues.png)
- PR #23, failed then passed: [`sonar-pr23-failed.png`](sonar-pr23-failed.png) · [`sonar-pr23-passed.png`](sonar-pr23-passed.png)
- The accepted issue, with its reason: [`sonar-l195-accepted.png`](sonar-l195-accepted.png)
- `main`, passed: [`sonar-main-passed.png`](sonar-main-passed.png)

**Still open, recorded on the gap list:** SonarQube reports 11 dependency
risks on `main` (rated E, but no gate condition is set on them), which Snyk's
check is not catching (see gap #4).

**What SonarQube found, in my words:** SonarQube found two secrets hardcoded in `app.py`. This is risky because anyone viewing a public repository could find and use them. I fixed the password issue and accepted the demo token because proper sign-in is planned for Week 3, gap #1.

**What this proves:** The tests passed, but SonarQube caught the hardcoded secrets. After I fixed the password, the gate failed because my new code had only 66.7% coverage, below the 80% requirement. I added a test, and then it passed.