#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
mkdir -p reports
# Format=opencover, because analyze.sh and thresholds.yml both name
# coverage.opencover.xml. Collecting the default cobertura is how a .NET
# learner ends up with the "coverage stuck at 0%" symptom that Week 0 §0.14
# lists among the eight common failures — the starter shipped the cause.
dotnet test --no-build -c Release profiles/dotnet \
  --collect:"XPlat Code Coverage;Format=opencover" \
  --results-directory reports \
  --logger "trx;LogFileName=test-results.trx"
echo "coverage report: reports/**/coverage.opencover.xml"
