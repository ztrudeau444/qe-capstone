#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
# The project file lives with the profile, not at the root.
dotnet restore profiles/dotnet
dotnet build --no-restore -c Release profiles/dotnet
