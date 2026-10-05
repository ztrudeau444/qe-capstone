#!/usr/bin/env bash
# Check that everything Week 0 asks for is actually present and working.
# Run this before Week 1 Day 1, and again whenever something stops working.
#
# Exit code is the number of REQUIRED items missing, so CI can gate on it.
set -uo pipefail

PROFILE="$(tr -d '[:space:]' < "$(dirname "$0")/../.qe-profile" 2>/dev/null || echo java)"
MISSING=0
WARN=0

bold() { printf '\033[1m%s\033[0m\n' "$1"; }
ok()   { printf '  \033[32m✓\033[0m %s\n' "$1"; }
bad()  { printf '  \033[31m✗\033[0m %s\n     → %s\n' "$1" "$2"; MISSING=$((MISSING+1)); }
warn() { printf '  \033[33m!\033[0m %s\n     → %s\n' "$1" "$2"; WARN=$((WARN+1)); }

# First version-looking number in a tool's --version output.
ver() {
  # Java 8's launcher rejects --version and prints nothing version-shaped,
  # so without the -version fallback $v comes back empty, the comparison is
  # skipped, and a JDK 8 is reported as satisfying "JDK 17+". Java 11 was
  # caught; Java 8 — the version an enterprise learner most likely has — was
  # not.
  local v
  v="$("$1" --version 2>&1 | grep -v '^Picked up' | grep -oE '[0-9]+(\.[0-9]+)+' | head -1)"
  [ -z "$v" ] && v="$("$1" -version 2>&1 | grep -v '^Picked up' | grep -oE '[0-9]+(\.[0-9]+)+' | head -1)"
  echo "$v"
}

need() {  # need <command> <human name> <fix hint> [minimum major version]
  if ! command -v "$1" >/dev/null 2>&1; then
    bad "$2 not found" "$3"
    return
  fi
  local v major
  v="$(ver "$1")"
  if [[ -n "${4:-}" && -n "$v" ]]; then
    major="${v%%.*}"
    if (( major < $4 )); then
      # An installed-but-too-old tool is worse than a missing one: everything
      # looks fine until a build fails for a reason nobody connects to this.
      bad "$2 is version $v — this program needs $4 or later" "$3"
      return
    fi
  fi
  ok "$2 — ${v:-installed}"
}

want() {  # optional
  if command -v "$1" >/dev/null 2>&1; then
    ok "$2"
  else
    warn "$2 not found (optional)" "$3"
  fi
}

bold "Core tooling"
need git    "Git (2.30+)" "https://git-scm.com/downloads" 2
need docker "Docker (20+)" "Docker Desktop, or Colima/Podman on Linux" 20

if command -v docker >/dev/null 2>&1; then
  if docker info >/dev/null 2>&1; then
    ok "Docker daemon is running"
    if docker compose version >/dev/null 2>&1; then
      ok "docker compose plugin present"
    else
      bad "docker compose not available" "Install the Compose plugin — 'docker-compose' with a hyphen is the old one"
    fi
  else
    # Installed but dead is its own failure, and a common one: 'docker --version'
    # answers happily while every command that matters times out.
    bad "Docker is installed but the daemon is not running" "Start Docker Desktop and re-run this script"
  fi
fi

bold "Language profile: $PROFILE"
case "$PROFILE" in
  java)
    need java "Java (JDK 17+)" "https://adoptium.net — install a JDK, not a JRE" 17
    need mvn  "Maven (3.9+)"    "https://maven.apache.org/install.html" 3
    if command -v javac >/dev/null 2>&1; then
      ok "javac present — this is a JDK, not a JRE"
    else
      bad "javac not found" "You have a JRE. Install a full JDK from https://adoptium.net"
    fi
    ;;
  python)
    need python3 "Python (3.11+)" "https://www.python.org/downloads/" 3
    need pip3    "pip"            "Ships with Python; try 'python3 -m ensurepip'"
    PYMINOR="$(python3 -c 'import sys;print(sys.version_info.minor)' 2>/dev/null || echo 0)"
    if (( PYMINOR < 11 )); then
      bad "Python 3.$PYMINOR is too old" "This program needs 3.11 or later"
    fi
    if [[ -n "${VIRTUAL_ENV:-}" ]]; then
      ok "Virtual environment active — $VIRTUAL_ENV"
    else
      warn "No virtual environment active" "python3 -m venv .venv && source .venv/bin/activate"
    fi
    ;;
  dotnet)
    need dotnet ".NET SDK (8+)" "https://dotnet.microsoft.com/download" 8
    ;;
  cpp)
    need cmake "CMake (3.16+)" "https://cmake.org/download/" 3
    need ctest "CTest (ships with CMake)" "https://cmake.org/download/"
    if command -v g++ >/dev/null 2>&1 || command -v clang++ >/dev/null 2>&1; then
      ok "C++ compiler present"
    else
      bad "No C++ compiler found" "Install g++ or clang++"
    fi
    # gcovr is how coverage gets out of gcov and into a report the pipeline
    # reads. Optional in the sense that build and test work without it; the
    # Analyze stage does not.
    if command -v gcovr >/dev/null 2>&1; then
      ok "gcovr — $(gcovr --version 2>/dev/null | head -1 | awk '{print $2}')"
    else
      warn "gcovr not found" "pip install gcovr — needed from Week 2 for coverage"
    fi
    ;;
  *)
    bad "Unknown profile '$PROFILE'" "Set .qe-profile to java, python, dotnet or cpp"
    ;;
esac

bold "Quality tooling (Weeks 2–4)"
want gh          "GitHub CLI"          "https://cli.github.com — makes Week 0 much faster"
want k6          "k6 (Week 3 load)"    "https://grafana.com/docs/k6/latest/set-up/install-k6/"
want node        "Node.js (Week 3 a11y tooling)" "https://nodejs.org — LTS"
want lighthouse  "Lighthouse CLI"      "npm i -g lighthouse"

bold "Repository state"
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  ok "Inside a Git repository"
  if git remote -v | grep -q origin; then
    ok "Remote 'origin' is set — $(git remote get-url origin)"
  else
    bad "No 'origin' remote" "git remote add origin <your repo URL>"
  fi
  BR="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo '?')"
  ok "On branch '$BR'"
  if [[ -f .env && ! -f .gitignore ]]; then
    bad ".env exists with no .gitignore" "You are one commit away from leaking credentials"
  fi
  if git ls-files --error-unmatch .env >/dev/null 2>&1; then
    bad ".env is TRACKED BY GIT" "git rm --cached .env  — then rotate anything that was in it"
  else
    ok ".env is not tracked"
  fi
else
  bad "Not a Git repository" "git init && git remote add origin <url>"
fi

bold "Connectivity"
if curl -sSf -m 10 https://github.com >/dev/null 2>&1; then
  ok "Can reach github.com"
else
  bad "Cannot reach github.com" "Check proxy / firewall — the pipeline will not run without this"
fi
if curl -sSf -m 10 https://sonarcloud.io >/dev/null 2>&1; then
  ok "Can reach SonarQube Cloud"
else
  warn "Cannot reach sonarcloud.io" "Week 2 Analyze stage needs this"
fi

echo
if [[ $MISSING -eq 0 && $WARN -eq 0 ]]; then
  bold "All clear. You are ready for Week 1."
elif [[ $MISSING -eq 0 ]]; then
  bold "Ready for Week 1. $WARN optional item(s) can wait until Week 3."
else
  bold "$MISSING required item(s) missing. Fix these before Day 1."
fi
exit $MISSING
