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

Integration tests were skipped on purpose, so coverage fell below the gate.
Every test that ran still passed: 2 · Test was green, 3 · Analyze was red.

- Failing run: [run 37817280239](https://github.com/ztrudeau444/qe-capstone/actions/runs/37817280239)
- Gate output: [`coverage-gate-failed.txt`](coverage-gate-failed.txt) · full log: [`coverage-gate-failed-full.log`](coverage-gate-failed-full.log)
- The PR could not merge while red (Task 4.5): [`pr-blocked-by-coverage-gate.png`](pr-blocked-by-coverage-gate.png)
- Restored by the revert commit in the same pull request; the run after it was green.

**What the log said, in my words:** <...>

**What this proves:** <...>