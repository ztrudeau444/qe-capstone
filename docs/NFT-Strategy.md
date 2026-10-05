# Non-Functional Test Strategy

Week 3. The tuning experiment at the bottom is the point of the week.

## Quality attributes in scope

| Attribute | Why it matters here | Metric | Target | Source |
|---|---|---|---|---|
| Performance | | p95 latency | ≤ 500 ms | k6 |
| Reliability | | error rate | < 1% | k6 |
| Security | | critical CVEs | 0 | Snyk + ZAP |
| Accessibility | | Lighthouse score | ≥ 95 | Lighthouse |

## Workload model

*The model is the skill. Defend each number.*

| | Value | Why this number |
|---|---|---|
| Peak concurrent users | | |
| Ramp-up | | |
| Steady-state duration | | |
| Scenario mix | | |
| Think time | | |

**Where the numbers came from:** <production analytics? a stakeholder estimate?
a guess? Say which — a defended guess is fine, an undisclosed one is not.>

## Baselines

| Metric | Week 1 | Week 2 | Week 3 first run | Week 3 after tuning |
|---|---|---|---|---|
| p95 latency | — | — | | |
| p99 latency | — | — | | |
| Error rate | — | — | | |
| Throughput | — | — | | |

## Security findings

| ID | Severity | Finding | Decision | Owner | Review by |
|---|---|---|---|---|---|
| | | | Fix / Accept / False positive | | |

*Every "Accept" also goes in `quality/thresholds.yml` under `security.accepted`
with the same expiry. Two places, because one is the record and the other is
the enforcement.*

## Accessibility findings

| Violation | Impact | Where | Fix | Status |
|---|---|---|---|---|
| | | | | |

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
| **Hypothesis** | *"p95 is high because …"* |
| **How you formed it** | Which dashboard, trace or profile pointed here? |
| **The one thing you changed** | |
| **Before** | p95 = , error rate = , throughput = |
| **After** | p95 = , error rate = , throughput = |
| **Did it confirm the hypothesis?** | |

**What you would try next.** <There is always a next bottleneck. Naming it shows
you understand the system rather than having found one lucky win.>
