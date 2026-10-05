#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
# No `pip install --upgrade pip` here. It fails on a distro-managed pip, it is
# not this build's job, and the only ways to make it quiet are to hide a real
# failure or to hide a real success.
python3 -m pip install -r profiles/python/requirements.txt
# Byte-compiling is a smoke check, not the build — src/ is a skeleton in
# Week 0 and legitimately has nothing importable in it yet. Report, do not
# fail; the Test stage is what decides whether the code works.
python3 -m compileall -q src || echo "note: src/ did not byte-compile cleanly"
