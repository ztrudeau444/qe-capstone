#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
mkdir -p reports

ctest --test-dir build/cpp --output-on-failure

# gcovr reads the .gcda files gcc wrote next to the objects and produces a
# Cobertura report, which is the format SonarQube Cloud and check-coverage.sh
# both understand.
gcovr --root . \
      --filter 'src/cpp/' \
      --exclude 'src/tests/' \
      --xml-pretty --output reports/coverage.xml \
      --txt=reports/coverage.txt --print-summary
echo "coverage report: reports/coverage.xml"
