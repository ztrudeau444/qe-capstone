#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
: "${SONAR_TOKEN:?SONAR_TOKEN is not set — Week 0 §0.7.2}"
# qualitygate.wait is what makes the gate a gate. Without it the scan
# uploads, the job exits 0, and the Quality Gate's verdict never reaches
# the pipeline — which is how the coverage gate came to be enforced by
# nothing at all.
mvn -B -ntp -f profiles/java/pom.xml sonar:sonar \
  -Dsonar.host.url=https://sonarcloud.io \
  -Dsonar.qualitygate.wait=true \
  -Dsonar.token="$SONAR_TOKEN"
