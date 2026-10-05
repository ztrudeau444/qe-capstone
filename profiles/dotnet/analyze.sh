#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
: "${SONAR_TOKEN:?SONAR_TOKEN is not set — Week 0 §0.7.2}"
: "${SONAR_PROJECT_KEY:?SONAR_PROJECT_KEY is not set}"
: "${SONAR_ORG:?SONAR_ORG is not set}"

# `|| true` is correct here and nowhere else in this repo: the tool being
# already installed is the success case, and it exits non-zero to say so.
dotnet tool install --global dotnet-sonarscanner 2>/dev/null || true
export PATH="$PATH:$HOME/.dotnet/tools"

dotnet sonarscanner begin   /d:sonar.qualitygate.wait=true \
  /k:"$SONAR_PROJECT_KEY" \
  /o:"$SONAR_ORG" \
  /d:sonar.token="$SONAR_TOKEN" \
  /d:sonar.host.url="https://sonarcloud.io" \
  /d:sonar.cs.opencover.reportsPaths="reports/**/coverage.opencover.xml"
dotnet build -c Release profiles/dotnet
dotnet sonarscanner end /d:sonar.token="$SONAR_TOKEN"
