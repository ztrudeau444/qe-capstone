#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
mkdir -p reports
python3 -m pip install --quiet -r profiles/python/requirements.txt
# -c names the profile's own config. Without it pytest reads no config from
# here at all, so branch coverage, testpaths and --strict-markers — every
# one of them set in profiles/python/pyproject.toml — silently do not apply,
# and branch_minimum becomes unmeasurable for this profile.
set +e
python3 -m pytest -c profiles/python/pyproject.toml \
  --cov=src \
  --cov-branch \
  --cov-report=xml:reports/coverage.xml \
  --cov-report=term-missing \
  --junitxml=reports/junit.xml
rc=$?
set -e

# pytest exit 5 is "no tests were collected", NOT a failure. The starter ships
# no application code by design, so a fresh checkout collects nothing — and
# Week 0 asks for one green pipeline run before Day 1. Without this a Python
# learner cannot get one, while a C++ learner can, because that profile ships a
# demo test. That asymmetry is the same wall P-17 was opened for, pointing the
# other way.
#
# It stops being tolerated the moment you have one test, which is Week 1 Day 2:
# pytest then returns 0 or 1 and this branch is never taken again.
if [ "$rc" -eq 5 ]; then
  echo "note: no tests collected yet. Expected before Week 1 — the starter"
  echo "      ships no application code of its own."
  exit 0
fi
[ "$rc" -ne 0 ] && exit "$rc"

echo "coverage report: reports/coverage.xml"
