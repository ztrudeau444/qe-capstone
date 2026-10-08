"""Fill in this week's measured numbers in docs/carry-forward-ledger.md.

Usage, from the repository root, with `docker compose up -d --wait` running:

    python scripts/update-ledger.py --week 2

It runs the whole test suite once, and only if every test passes, writes into
the Four-week trend column for that week:

    Line coverage %, Branch coverage %   (TalkDesk's code only, never the tests)
    Unit tests, Integration tests, E2E tests, Suite runtime (s)
    Criteria covered                     (ticked rows in docs/acceptance-criteria.md)

It also prints the commit count for the week's "Repository" record.

What it deliberately leaves to you: every tick box, the instructor lines, the
"Carried into" notes, and anything a script cannot measure (Maintainability
grade, pipeline stages, load, security and accessibility numbers). A tick is a
judgement, not a measurement.
"""
import argparse
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "carry-forward-ledger.md"
CRITERIA = ROOT / "docs" / "acceptance-criteria.md"
REPORTS = ROOT / "reports"
JUNIT = REPORTS / "ledger-junit.xml"
COVERAGE = REPORTS / "ledger-coverage.json"


def run_suite():
    """Run every test once. Returns True only if the whole suite passed."""
    REPORTS.mkdir(exist_ok=True)
    cmd = [sys.executable, "-m", "pytest", "-c", "profiles/python/pyproject.toml",
           "src/tests", "-q", "-p", "no:cacheprovider",
           # Coverage of TalkDesk's code only. --cov-config makes the omit and
           # branch settings in the profile's pyproject.toml actually apply.
           "--cov=src/talkdesk", "--cov-branch",
           "--cov-config=profiles/python/pyproject.toml",
           f"--cov-report=json:{COVERAGE}", "--cov-report=",
           f"--junitxml={JUNIT}"]
    return subprocess.run(cmd, cwd=ROOT).returncode == 0


def count_tests(junit_path):
    """Unit / integration / e2e counts and total runtime, from the JUnit report."""
    root = ET.parse(junit_path).getroot()
    suite = root if root.tag == "testsuite" else root.find("testsuite")
    counts = {"unit": 0, "integration": 0, "e2e": 0}
    for case in suite.iter("testcase"):
        parts = case.get("classname", "").split(".")
        for layer in counts:
            if layer in parts:
                counts[layer] += 1
                break
    return counts, float(suite.get("time", 0))


def coverage_percent(coverage_path):
    totals = json.loads(Path(coverage_path).read_text(encoding="utf-8"))["totals"]
    line = 100 * totals["covered_lines"] / max(totals["num_statements"], 1)
    branch = 100 * totals["covered_branches"] / max(totals["num_branches"], 1)
    return round(line), round(branch)


def criteria_covered(criteria_text):
    """(ticked, total) from the traceability table at the end of the criteria file."""
    rows = [l for l in criteria_text.splitlines() if re.match(r"\|\s*AC-\d+\s*\|", l)]
    return sum("☒" in r for r in rows), len(rows)


def commit_count():
    out = subprocess.run(["git", "rev-list", "--count", "HEAD"], cwd=ROOT,
                         capture_output=True, text=True)
    return out.stdout.strip() or "?"


def write_trend(ledger_text, week, values):
    """Replace this week's cell in each named row of the Four-week trend table.
    Returns the new text and a list of (metric, old, new) changes."""
    start = ledger_text.index("# Four-week trend")
    end = ledger_text.find("\n---", start)
    end = len(ledger_text) if end == -1 else end
    lines = ledger_text[start:end].split("\n")
    changes = []
    for i, line in enumerate(lines):
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        metric = cells[0].strip("* ")
        if metric in values:
            old, new = cells[week], values[metric]
            if new is None or old == new:
                continue
            cells[week] = new
            lines[i] = "| " + " | ".join(cells) + " |"
            changes.append((metric, old or "(blank)", new))
    return ledger_text[:start] + "\n".join(lines) + ledger_text[end:], changes


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--week", type=int, required=True, choices=[1, 2, 3, 4])
    args = parser.parse_args()

    if not run_suite():
        sys.exit("\nNot updated: the suite is not green. A ledger records what "
                 "passed, so fix the failure first.\n(Integration tests need the "
                 "database: docker compose up -d --wait)")

    counts, runtime = count_tests(JUNIT)
    line, branch = coverage_percent(COVERAGE)
    ticked, total = criteria_covered(CRITERIA.read_text(encoding="utf-8"))

    def count(n):
        # Week 1's template shows "—" for layers that do not exist yet; keep it.
        return str(n) if n or args.week > 1 else None

    values = {
        "Line coverage %": str(line),
        "Branch coverage %": str(branch),
        "Unit tests": str(counts["unit"]),
        "Integration tests": count(counts["integration"]),
        "E2E tests": count(counts["e2e"]),
        "Suite runtime (s)": f"{runtime:.1f}",
        "Criteria covered": f"{ticked}/{total}",
    }
    text, changes = write_trend(LEDGER.read_text(encoding="utf-8"), args.week, values)
    LEDGER.write_text(text, encoding="utf-8")

    print(f"\nWeek {args.week} trend column:")
    for metric, old, new in changes or [("(nothing changed)", "", "")]:
        print(f"  {metric:<20} {old:>10} -> {new}")
    print(f"\nFor the Week {args.week} records (fill in by hand):")
    print(f"  Commits on this branch: {commit_count()}")
    print(f"  Tests: unit {counts['unit']}, integration {counts['integration']}, "
          f"e2e {counts['e2e']}  ·  runtime {runtime:.1f} s")
    print(f"  Criteria with a test: {ticked} of {total}")
    print("\nTicks, notes and unmeasured cells are yours. Review with: git diff docs/")


if __name__ == "__main__":
    main()