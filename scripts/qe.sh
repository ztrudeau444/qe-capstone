#!/usr/bin/env bash
# Dispatch a task to the active language profile.
#
#   ./scripts/qe.sh build|test|analyze
#
# The pipeline calls this, never a build tool directly. That is deliberate:
# the workflow should not know whether this project is Maven or pytest.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TASK="${1:-}"

if [[ -z "$TASK" ]]; then
  echo "usage: $0 <build|test|analyze>" >&2
  exit 64
fi

PROFILE_FILE="$ROOT/.qe-profile"
if [[ ! -f "$PROFILE_FILE" ]]; then
  echo "No .qe-profile found. Write one of: java, python, dotnet, cpp" >&2
  exit 78
fi

PROFILE="$(tr -d '[:space:]' < "$PROFILE_FILE")"
SCRIPT="$ROOT/profiles/$PROFILE/$TASK.sh"

if [[ ! -x "$SCRIPT" ]]; then
  echo "No task '$TASK' for profile '$PROFILE' (looked for $SCRIPT)" >&2
  echo "Available profiles: $(cd "$ROOT/profiles" && ls -d */ | tr -d / | tr '\n' ' ')" >&2
  exit 78
fi

echo "==> [$PROFILE] $TASK"
exec "$SCRIPT"
