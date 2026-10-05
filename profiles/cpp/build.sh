#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."

# Out-of-source build. Everything generated lands in build/, which is
# gitignored, so a clean checkout is genuinely clean.
cmake -S profiles/cpp -B build/cpp -DCMAKE_BUILD_TYPE=Debug
cmake --build build/cpp --parallel
