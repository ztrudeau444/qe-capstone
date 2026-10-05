#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
: "${SONAR_TOKEN:?SONAR_TOKEN is not set — Week 0 §0.7.2}"
: "${SONAR_PROJECT_KEY:?SONAR_PROJECT_KEY is not set — Week 0 §0.7.2}"
: "${SONAR_ORG:?SONAR_ORG is not set — Week 0 §0.7.2}"

# Passed on the command line, not read from sonar-project.properties, because
# that file ships placeholders and a learner who correctly set the repository
# variables would otherwise still be analysing YOUR_ORG_your-repo.
#
# sonar-scanner is installed by the CI workflow's setup-profile action; locally,
# brew install sonar-scanner or use the Docker image.
sonar-scanner   -Dsonar.projectKey="$SONAR_PROJECT_KEY"   -Dsonar.organization="$SONAR_ORG"   -Dsonar.host.url=https://sonarcloud.io   -Dsonar.qualitygate.wait=true   -Dsonar.token="$SONAR_TOKEN"
