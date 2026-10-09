"""One-off helper: response times per address, from a k6 CSV results file.

k6's summary shows one p95 for ALL requests mixed together. This splits the
results by the `name` tag each request carries in load.js (for example
"GET /api/talks"), so you can see which address is slow.

Usage, from the project folder:
    python ~/k6_by_endpoint.py reports/load-full.csv
"""
import csv
import logging
import sys
from collections import defaultdict

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger("k6_by_endpoint")


def percentile(sorted_values, p):
    """Return the value below which p% of the (already sorted) values fall.

    Uses the "nearest rank" method. k6 interpolates slightly differently, so
    expect small differences from k6's own summary, not large ones.
    """
    if not sorted_values:
        return 0.0
    rank = max(1, round(p / 100 * len(sorted_values)))
    return sorted_values[rank - 1]


def main():
    """Read the CSV, group request durations by address, print a table.

    Steps:
      1. Read every row of the CSV, keeping only http_req_duration rows
         (one per request; the file holds many other metrics too).
      2. Group the durations by the request's `name` tag, leaving out the
         one-off setup request.
      3. For each address, print how many requests, its share of all
         requests, and p50 / p95 / p99 / max in milliseconds.
    """
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python ~/k6_by_endpoint.py reports/load-full.csv")
    path = sys.argv[1]

    # Steps 1 and 2: collect durations per address.
    log.info("Reading %s", path)
    durations = defaultdict(list)
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["metric_name"] == "http_req_duration" and row["name"] != "setup":
                durations[row["name"]].append(float(row["metric_value"]))
    total = sum(len(v) for v in durations.values())
    log.info("Found %d requests across %d addresses", total, len(durations))

    # Step 3: one line per address, slowest p95 first.
    header = f"{'Address':<26}{'Requests':>9}{'Share':>8}{'p50':>9}{'p95':>9}{'p99':>9}{'max':>9}"
    print("\n" + header + "\n" + "-" * len(header))
    rows = []
    for name, values in durations.items():
        values.sort()
        rows.append((name, len(values), percentile(values, 50), percentile(values, 95),
                     percentile(values, 99), values[-1]))
    for name, n, p50, p95, p99, mx in sorted(rows, key=lambda r: r[3], reverse=True):
        print(f"{name:<26}{n:>9}{n / total:>8.0%}{p50:>8.0f}ms{p95:>7.0f}ms{p99:>7.0f}ms{mx:>7.0f}ms")
    print("\nAll times in milliseconds. Gate: p95 <= 500 ms (applies to all requests together).")


if __name__ == "__main__":
    main()