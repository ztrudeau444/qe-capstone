#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
# The POM lives with the profile, not at the root, so name it explicitly.
# Without -f this fails with "there is no POM in this directory".
mvn -B -ntp -f profiles/java/pom.xml clean compile
