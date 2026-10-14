"""Unit tests: check-a11y.py counts every violation (gap list #24).

Line 26 read `counts.get(impact, 0) + len(nodes) or 1`. Python does the `+`
before the `or`, so the "count at least 1" fallback only applied when the
running total was 0. A second violation with no nodes listed added nothing,
so the gate could pass with more violations than its limit.
The script is run as a separate program, the same way the pipeline runs it.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[3] / "scripts" / "check-a11y.py"


def run_check(tmp_path, violations, max_critical="0"):
    """Write a small fake axe report and run the real script on it."""
    report = tmp_path / "axe.json"
    report.write_text(json.dumps({"violations": violations}))
    env = {**os.environ, "MAX_CRITICAL": max_critical, "MAX_SERIOUS": "0"}
    return subprocess.run([sys.executable, str(SCRIPT), str(report)],
                          capture_output=True, text=True, env=env)


def test_no_violations_passes(tmp_path):
    r = run_check(tmp_path, [])
    assert r.returncode == 0
    assert "critical: 0" in r.stdout


def test_each_affected_element_is_counted(tmp_path):
    r = run_check(tmp_path, [{"impact": "critical", "nodes": [{}, {}, {}]}],
                  max_critical="5")
    assert "critical: 3" in r.stdout


def test_violations_without_nodes_each_count_as_one(tmp_path):
    two = [{"impact": "critical", "nodes": []},
           {"impact": "critical", "nodes": []}]
    r = run_check(tmp_path, two, max_critical="1")
    assert "critical: 2" in r.stdout
    assert r.returncode == 1, "two critical violations got past a limit of 1"