#!/usr/bin/env bash
#
# The coverage gate, enforced rather than announced.
#
# This exists because the Analyze stage used to print "Coverage gate: >= 80%"
# and pass regardless. Week 2's exit gate asks for "a failing run that proves
# the gate bites", and a stage that cannot fail cannot produce one.
#
# Thresholds come from the environment, which the workflow fills from
# quality/thresholds.yml. Nothing is hard-coded here — that is rule 1 of that
# file, and this script is not an exception to it.
set -euo pipefail
cd "$(dirname "$0")/.."

MIN="${COVERAGE_MIN:?COVERAGE_MIN is not set}"
BRANCH_MIN="${BRANCH_MIN:-0}"

# Find whichever report this profile produced.
REPORT=""
for candidate in     reports/coverage.xml     target/site/jacoco/jacoco.xml     reports/**/coverage.opencover.xml; do
  for f in $candidate; do
    [[ -f "$f" ]] && REPORT="$f" && break 2
  done
done

if [[ -z "$REPORT" ]]; then
  echo "::error::No coverage report found. Did the Test stage run?" >&2
  echo "Looked for reports/coverage.xml, target/site/jacoco/jacoco.xml," >&2
  echo "and reports/**/coverage.opencover.xml." >&2
  exit 1
fi

echo "Reading $REPORT"

read -r LINE_PCT BRANCH_PCT < <(python3 - "$REPORT" <<'PY'
import sys, xml.etree.ElementTree as ET

root = ET.parse(sys.argv[1]).getroot()

def pct(covered, missed):
    total = covered + missed
    return 100.0 * covered / total if total else 100.0

line = branch = None

# Cobertura / coverage.py both carry rates on the root element.
if root.get("line-rate") is not None:
    line = float(root.get("line-rate")) * 100
    if root.get("branch-rate") is not None:
        branch = float(root.get("branch-rate")) * 100

# JaCoCo carries counters as children of the report element.
for c in root.findall("counter"):
    if c.get("type") == "LINE":
        line = pct(int(c.get("covered")), int(c.get("missed")))
    if c.get("type") == "BRANCH":
        branch = pct(int(c.get("covered")), int(c.get("missed")))

# OpenCover carries a summary element.
s = root.find("Summary")
if s is not None:
    if s.get("sequenceCoverage") is not None:
        line = float(s.get("sequenceCoverage"))
    if s.get("branchCoverage") is not None:
        branch = float(s.get("branchCoverage"))

if line is None:
    sys.exit("could not read line coverage from this report")
print(f"{line:.2f} {branch if branch is not None else -1:.2f}")
PY
)

FAIL=0
printf 'Line coverage:   %6.2f%%   (gate: >= %s%%)
' "$LINE_PCT" "$MIN"
awk -v a="$LINE_PCT" -v b="$MIN" 'BEGIN{exit !(a+0 < b+0)}' && {
  echo "::error::Line coverage $LINE_PCT% is below the gate of $MIN%."
  FAIL=1
}

if awk -v b="$BRANCH_PCT" 'BEGIN{exit !(b+0 >= 0)}'; then
  printf 'Branch coverage: %6.2f%%   (gate: >= %s%%)
' "$BRANCH_PCT" "$BRANCH_MIN"
  awk -v a="$BRANCH_PCT" -v b="$BRANCH_MIN" 'BEGIN{exit !(a+0 < b+0)}' && {
    echo "::error::Branch coverage $BRANCH_PCT% is below the gate of $BRANCH_MIN%."
    FAIL=1
  }
else
  echo "Branch coverage: not reported by this profile's coverage tool."
fi

if [[ $FAIL -eq 0 ]]; then
  echo "Coverage gates met."
fi
exit $FAIL
