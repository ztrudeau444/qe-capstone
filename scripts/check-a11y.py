#!/usr/bin/env python3
'''Judge an axe-core report against the thresholds this program declares.

The A11y stage used to run `axe --exit`, which fails on ANY violation. That is
stricter than the limits in quality/thresholds.yml, it is not read from that
file, and a rule the pipeline enforces but nobody wrote down is a rule nobody
can argue with. This reads the report and applies the declared limits.

    MAX_CRITICAL=0 MAX_SERIOUS=0 python3 scripts/check-a11y.py reports/axe.json
'''
import json
import os
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "reports/axe.json"
try:
    data = json.load(open(path))
except (OSError, json.JSONDecodeError) as e:
    sys.exit(f"::error::cannot read {path}: {e}")

runs = data if isinstance(data, list) else [data]
counts = {"critical": 0, "serious": 0, "moderate": 0, "minor": 0}
for run in runs:
    for v in run.get("violations", []):
        impact = v.get("impact") or "minor"
        counts[impact] = counts.get(impact, 0) + len(v.get("nodes", [])) or 1

max_critical = int(os.environ.get("MAX_CRITICAL", 0))
max_serious = int(os.environ.get("MAX_SERIOUS", 0))

for impact in ("critical", "serious", "moderate", "minor"):
    print(f"{impact:>9}: {counts.get(impact, 0)}")
print(f"gates: critical <= {max_critical}, serious <= {max_serious}")

failed = False
if counts.get("critical", 0) > max_critical:
    print(f"::error::{counts['critical']} critical violations "
          f"(limit {max_critical})")
    failed = True
if counts.get("serious", 0) > max_serious:
    print(f"::error::{counts['serious']} serious violations "
          f"(limit {max_serious})")
    failed = True

if not failed:
    print("Accessibility violation gates met.")
    print("A passing gate is not the same as an accessible page — automation "
          "covers roughly a third of WCAG success criteria. The keyboard pass
"
          "is yours.")
sys.exit(1 if failed else 0)
