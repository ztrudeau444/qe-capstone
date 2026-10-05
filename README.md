# Quality Engineering Program — Starter Repository

This is the repository you carry through all four weeks. It is deliberately
**empty of application code**: the System Under Test is yours. What is supplied
is the scaffolding around it — the pipeline, the quality gates, the framework
skeleton and the documents you fill in as you go.

## First five minutes

```bash
./scripts/verify-setup.sh          # tells you what is missing before you start
echo java > .qe-profile            # java | python | dotnet | cpp  (pick one)
./scripts/qe.sh build              # should succeed and do nothing much
```

If `verify-setup.sh` reports anything missing, fix that before Week 1 Day 1.
The Week 0 guide explains every item it checks.

## How the language dispatch works

The pipeline never mentions Maven, pytest or `dotnet`. It calls tasks:

```
./scripts/qe.sh build
./scripts/qe.sh test
./scripts/qe.sh analyze
```

`scripts/qe.sh` reads `.qe-profile` and runs `profiles/<profile>/<task>.sh`.

This is the same idea the readers argue for in Week 2 §3: **depend on the
abstraction, not the tool.** Swapping Maven for Gradle changes one file in
`profiles/java/` and nothing in `.github/workflows/ci.yml`. If you find yourself
adding a language `if` to the workflow, you have put the knowledge in the wrong
place.

## Layout

| Path | What lives here | First used |
|---|---|---|
| `src/` | Your framework layers — see `src/README.md` | Week 1 |
| `profiles/` | Per-language build/test/analyze commands | Week 1 |
| `quality/thresholds.yml` | **Every quality gate, in one file** | Week 2 |
| `quality/performance/` | k6 scripts — load, stress, smoke | Week 3 |
| `quality/security/` | ZAP and Snyk configuration | Week 3 |
| `quality/accessibility/` | axe, Pa11y and Lighthouse configuration | Week 3 |
| `.github/workflows/ci.yml` | The eight-stage pipeline | Week 2 |
| `docs/` | The documents you are assessed on | Week 1 onward |

## The eight stages

```
Build → Test → Analyze → LoadTest → Security → A11y → Deploy → Smoke
  W2      W2      W2         W3        W3       W3      W4      W4
```

Stages you have not reached yet are present but skipped, so you can see the
shape of the finished thing from day one. Turn each on by setting its flag in
`quality/thresholds.yml`.

## A note on what is not here

There is no application. There is no reference System Under Test in this
repository — you choose your own on Week 1, Day 1, against the criteria in
Week 1 §0.2, and it must survive four weeks rather than one.

If your own choice collapses, tell your instructor. Do not silently start again
with something smaller in Week 3; the whole assessment is the trend line.
