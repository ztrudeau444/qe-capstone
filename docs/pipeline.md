# Pipeline

Week 2 onward. One row per stage. A stage with no stated failure behaviour is a
stage nobody has thought through.

## The eight stages

```
Build → Test → Analyze → LoadTest → Security → A11y → Deploy → Smoke
```

| # | Stage | Trigger | Input | Gate | On failure | Turned on |
|---|---|---|---|---|---|---|
| 1 | Build | push, PR | source | compiles | block | Week 2, <date> |
| 2 | Test | after Build | artifact + DB service | all green | block | Week 2, <date> |
| 3 | Analyze | after Test | coverage report | ≥ 80% line, Grade A | block | Week 2, <date> |
| 4 | LoadTest | after Analyze | running container | p95 ≤ 500 ms, errors < 1% | block | Week 3, <date> |
| 5 | Security | after Analyze | deps + running container | 0 critical, 0 high | block | Week 3, <date> |
| 6 | A11y | after Analyze | running container | Lighthouse ≥ 95 | block | Week 3, <date> |
| 7 | Deploy | gates green | image | deploy succeeds | block | Week 4, <date> |
| 8 | Smoke | after Deploy | staging URL | all checks pass | roll back | Week 4, <date> |

**Fill in the dates.** They are the trend line — the Week 4 metrics report reads
this column.

## Runtime

| | Target | Actual |
|---|---|---|
| Pull-request feedback (stages 1–3) | < 10 min | |
| Full pipeline | < 25 min | |

If pull-request feedback exceeds ten minutes, people stop waiting for it and
start merging on hope. Record what you did about it.

## What runs nightly instead

Soak test and mutation testing live in `nightly.yml`. Say why each is there
rather than in the pull-request path.

## Version currency

Actions are pinned to major tags. Check them once a term:

| Action | Pinned | Last checked |
|---|---|---|
| `actions/checkout` | v6 | |
| `actions/setup-java` | v5 | |
| `actions/setup-python` | v5 | |
| `actions/setup-dotnet` | v4 | |
| `grafana/setup-k6-action` | v1 | |
| `zaproxy/action-baseline` | v0.15.0 | |
