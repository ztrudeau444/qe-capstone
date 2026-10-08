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

**What the log said, in my words:** <What the log said, in my words: Line coverage dropped to 54.84% and branch coverage to 40%, both below the gates of 80% and 60%, so the Analyze stage failed even though every test that ran passed.>

**What this proves:** <What this proves: The gate really blocks a change that leaves too much code untested, even when every test passes, and the pipeline goes back to green as soon as the tests are restored.>


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
