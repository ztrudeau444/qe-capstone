#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
# jacoco:report is bound to the verify phase in pom.xml
mvn -B -ntp -f profiles/java/pom.xml verify
echo "coverage report: target/site/jacoco/jacoco.xml"
