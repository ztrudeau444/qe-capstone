"""Dashboard for one k6 load run: p50, p95, p99 and throughput over time.

Reads the CSV that `k6 run --out csv=...` writes and saves a two-panel chart:
  top    - response time percentiles (p50, p95, p99) per 10-second window
  bottom - throughput (requests per second) per 10-second window

Usage:
  python scripts/k6-dashboard.py <k6.csv> <output.png> "<label>"
"""
import csv
import math
import sys

import matplotlib

matplotlib.use("Agg")  # draw straight to a file, no window
import matplotlib.pyplot as plt

WINDOW = 10        # seconds per point on the chart
GATE_P95_MS = 500  # the pipeline gate, from quality/thresholds.yml


def pct(sorted_vals, p):
    """Percentile with linear interpolation (the same method k6 uses)."""
    k = (len(sorted_vals) - 1) * p / 100
    f = math.floor(k)
    c = min(f + 1, len(sorted_vals) - 1)
    return sorted_vals[f] + (sorted_vals[c] - sorted_vals[f]) * (k - f)


def main(csv_path, png_path, label):
    per_second = {}   # unix second -> list of durations (ms)
    failed = total = 0
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            name = row["metric_name"]
            if name == "http_req_duration":
                t = int(float(row["timestamp"]))
                per_second.setdefault(t, []).append(float(row["metric_value"]))
            elif name == "http_req_failed":
                total += 1
                failed += float(row["metric_value"])

    if not per_second:
        sys.exit("No http_req_duration rows found - is this a k6 CSV?")

    start, end = min(per_second), max(per_second)
    windows = {}
    for t, vals in per_second.items():
        windows.setdefault((t - start) // WINDOW, []).extend(vals)

    xs, p50, p95, p99, rps = [], [], [], [], []
    for w in sorted(windows):
        vals = sorted(windows[w])
        xs.append(w * WINDOW / 60)  # minutes into the run
        p50.append(pct(vals, 50))
        p95.append(pct(vals, 95))
        p99.append(pct(vals, 99))
        rps.append(len(vals) / WINDOW)

    everything = sorted(v for vals in per_second.values() for v in vals)
    o50, o95, o99 = (pct(everything, p) for p in (50, 95, 99))
    avg_rps = len(everything) / (end - start + 1)
    err = failed / total if total else 0.0

    fig, (top, bottom) = plt.subplots(
        2, 1, figsize=(11, 7), sharex=True, gridspec_kw={"height_ratios": [3, 2]})
    top.plot(xs, p50, color="#2a9d8f", label=f"p50 (whole run {o50:.0f} ms)")
    top.plot(xs, p95, color="#e9a23b", label=f"p95 (whole run {o95:.0f} ms)")
    top.plot(xs, p99, color="#d1495b", label=f"p99 (whole run {o99:.0f} ms)")
    if max(p99) >= GATE_P95_MS * 0.8:  # only draw the gate when it's in view
        top.axhline(GATE_P95_MS, color="grey", linestyle="--",
                    label=f"gate: p95 <= {GATE_P95_MS} ms")
    top.set_ylabel("Response time (ms)")
    top.set_ylim(bottom=0)
    top.grid(alpha=0.3)
    top.legend(loc="upper left")

    bottom.plot(xs, rps, color="#264653",
                label=f"throughput (average {avg_rps:.1f} req/s)")
    bottom.set_ylabel("Requests per second")
    bottom.set_xlabel("Minutes into the run")
    bottom.set_ylim(bottom=0)
    bottom.grid(alpha=0.3)
    bottom.legend(loc="upper left")

    fig.suptitle(f"TalkDesk load test - {label}\n"
                 f"{len(everything):,} requests, error rate {err:.2%}, "
                 f"{WINDOW}-second windows")
    fig.tight_layout()
    fig.savefig(png_path, dpi=120)

    print(f"{label}: p50={o50:.0f} ms  p95={o95:.0f} ms  p99={o99:.0f} ms  "
          f"throughput={avg_rps:.1f} req/s  errors={err:.2%}  "
          f"requests={len(everything):,}")
    print(f"Saved {png_path}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(*sys.argv[1:])