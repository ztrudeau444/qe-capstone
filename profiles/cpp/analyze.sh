#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
: "${SONAR_TOKEN:?SONAR_TOKEN is not set — Week 0 §0.7}"
: "${SONAR_PROJECT_KEY:?SONAR_PROJECT_KEY is not set — Week 0 §0.7.2}"
: "${SONAR_ORG:?SONAR_ORG is not set — Week 0 §0.7.2}"

# C++ is the one profile where Sonar needs more than a scanner.
#
# SonarQube's C++ analyser cannot infer how your code was compiled — there is no
# equivalent of a POM or a csproj to read. It needs a compilation database, and
# the build-wrapper is what produces one. This is a real extra step and the
# other three profiles do not have it; that asymmetry is the honest cost of C++
# support, not something the program is hiding.
#
# Two ways to give it one:
#   1. CMake emits compile_commands.json for free (set below), which the
#      analyser accepts via sonar.cfamily.compile-commands.
#   2. Or wrap the build: build-wrapper-linux-x86-64 --out-dir bw-output <build>
#
# Option 1 needs no extra download, so it is what the starter uses.
cmake -S profiles/cpp -B build/cpp -DCMAKE_EXPORT_COMPILE_COMMANDS=ON >/dev/null
cmake --build build/cpp --parallel >/dev/null

sonar-scanner \
  -Dsonar.projectKey="$SONAR_PROJECT_KEY" \
  -Dsonar.organization="$SONAR_ORG" \
  -Dsonar.host.url=https://sonarcloud.io \
  -Dsonar.sources=src/cpp \
  -Dsonar.tests=src/tests/unit/cpp \
  -Dsonar.cfamily.compile-commands=build/cpp/compile_commands.json \
  -Dsonar.coverageReportPaths=reports/coverage.xml \
  -Dsonar.qualitygate.wait=true \
  -Dsonar.token="$SONAR_TOKEN"
