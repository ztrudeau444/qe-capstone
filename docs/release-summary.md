# Release Summary

Week 4. One page. This is what you hand to somebody who has to decide whether
this ships — and it is the front page of your defence.

**Write it last.** Everything else feeds it.

## The system

<Two sentences. What it does, who uses it. No jargon — assume the reader
controls budget and has never opened a test report.>

## What is verified

| Layer | What it actually catches | Where the evidence is |
|---|---|---|
| Unit | | |
| Integration | | |
| End-to-end | | |
| Load | | |
| Security | | |
| Accessibility | | |

## The numbers

| Metric | Result | Gate | Met |
|---|---|---|---|
| Line coverage | | ≥ 80% | ☐ |
| Branch coverage | | ≥ 60% | ☐ |
| Maintainability | | Grade A | ☐ |
| p95 latency | | ≤ 500 ms | ☐ |
| Error rate under load | | < 1% | ☐ |
| Critical CVEs | | 0 | ☐ |
| High CVEs | | 0 | ☐ |
| Accessibility | | ≥ 95 | ☐ |
| Functional criteria covered | | 100% | ☐ |

## What is **not** verified

*Named. Specifically. This is the section that earns trust — a reader who finds
an uncovered area you did not disclose stops believing the section above it.*

- …

## Known risk carried

| Risk | Why accepted | What would change the decision | Owner |
|---|---|---|---|
| | | | |

## Evidence

| | Link |
|---|---|
| Pipeline run — all eight stages green from one commit | |
| Metrics report | `docs/metrics-report.md` |
| Dashboards | |
| Gap list | `docs/gap-list.md` |

---

**A note on order.** *What is not verified* comes before *known risk* deliberately.
They are different things — a coverage gap is something nobody looked at; an
accepted risk is something somebody looked at and decided to carry. A reader who
conflates them will over-trust the numbers table.
