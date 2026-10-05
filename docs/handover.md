# Hand-over

Week 4. Written as though you were rolling off tomorrow and someone else were
inheriting this. On a real engagement this is the document that decides whether
your work survives you.

## What this system is

<Two sentences. What it does, who uses it.>

## Running it

```bash
# from a clean clone
./scripts/verify-setup.sh
docker compose up -d --wait
```

## Running the tests

| What | Command | Takes |
|---|---|---|
| Unit | | |
| Integration | | |
| E2E | | |
| Smoke against staging | | |
| Load | | |

## Reading the dashboards

| Dashboard | Where | What "normal" looks like |
|---|---|---|
| SonarQube Cloud | | |
| Grafana | | |
| Pipeline | | |

## The quality gates

All thresholds live in `quality/thresholds.yml`. Changing one requires review —
see `.github/CODEOWNERS`.

## What is deliberately not covered

<Be specific. "Everything is tested" is never true and reviewers know it.>

## The three things most likely to break first

| # | What | Why | Early warning |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |

## Who to ask

| Topic | Person |
|---|---|
| | |
