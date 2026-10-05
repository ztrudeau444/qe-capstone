#!/usr/bin/env bash
#
# Verify a Week 5 certificate against the repository it names.
#
# It checks four things, reads all of them FROM THE NAMED COMMIT, and is
# explicit about the one thing it cannot check:
#
#   1. the commit exists and is reachable from a branch or tag
#   2. every file the manifest lists is present in that commit, unchanged
#   3. no evidence file was ADDED to that commit's evidence/ after the manifest
#   4. the manifest's own hash matches the one on the certificate
#
# It CANNOT check whether the assessment was any good. Nothing can. That is why
# the certificate names its assessor.
#
#   ./scripts/verify-certificate.sh <commit-sha> <manifest-sha256>
#
# Both arguments are required. Run with a commit alone and it will print the
# manifest hash for you and exit non-zero, because a run that checked nothing
# against a certificate must not print "Verified".
#
# HISTORY, because it is the point of the exercise. The first version of this
# script ran `sha256sum --check` in the working tree and then printed "the
# evidence is intact and matches the assessed commit" — a sentence nothing in it
# had established. A commit containing no evidence directory at all, plus
# fabricated untracked files on disk, passed it cleanly. Everything below reads
# through `git show <commit>:` for that reason.
#
set -euo pipefail
cd "$(dirname "$0")/.."

COMMIT="${1:-}"
EXPECTED_MANIFEST="${2:-}"

if [[ -z "$COMMIT" ]]; then
  echo "usage: $0 <commit-sha> <expected-manifest-sha256>" >&2
  exit 64
fi

fail=0
say() { printf '%s\n' "$*"; }

# ---------------------------------------------------------------- 1. commit
#
# Two questions, not one. `cat-file -e` answers "is this object in the
# database", which stays true for a commit orphaned by a force-push until git
# gc runs — the exact case this check exists to catch.
#
# Reachability must be asked of REFS ONLY. `git branch -a --contains` reports
# the detached HEAD itself, and `git checkout <commit>` — which is what the
# certificate template tells a verifier to do — produces exactly that. The
# second version of this check used it and therefore passed every orphaned
# commit a verifier following the published procedure would ever look at.
if ! git cat-file -e "${COMMIT}^{commit}" 2>/dev/null; then
  say "FAIL  commit $COMMIT is not in this repository at all"
  say "      Either the certificate names the wrong repository, or you have not"
  say "      fetched its history. Try: git fetch --all --tags"
  exit 1
fi

refs="$(git for-each-ref --contains "$COMMIT" --format='%(refname)' \
          refs/heads refs/remotes refs/tags 2>/dev/null || true)"
if [[ -n "$refs" ]]; then
  say "ok    commit ${COMMIT:0:12} exists and is reachable from a ref"
  say "      $(git log -1 --format='%ci  %s' "$COMMIT")"
else
  say "FAIL  commit $COMMIT exists but is NOT reachable from any branch or tag"
  say "      This is what a force-push after issue looks like. The object is"
  say "      still in your local database; it is in nobody else's clone."
  fail=1
fi

# ------------------------------------------------------------- 2. evidence
#
# Everything from here reads the commit's tree. Nothing reads the working tree.
if ! git cat-file -e "${COMMIT}:evidence/manifest.sha256" 2>/dev/null; then
  say "FAIL  that commit contains no evidence/manifest.sha256"
  say "      The manifest must be committed. A manifest generated after the"
  say "      last commit is not part of what was assessed."
  exit 1
fi

manifest="$(git show "${COMMIT}:evidence/manifest.sha256")"

if [[ -z "${manifest//[[:space:]]/}" ]]; then
  say "FAIL  the manifest in that commit is empty — nothing to verify"
  exit 1
fi

listed=0
missing=0
changed=0
declare -a listed_paths=()

while IFS= read -r line; do
  [[ -z "${line//[[:space:]]/}" ]] && continue
  # sha256sum prefixes a line with a backslash when the filename contains one
  # or a newline. Those are legal and the escaping is not worth decoding here;
  # refuse rather than quietly skip.
  if [[ "$line" == \\* ]]; then
    say "FAIL  manifest contains an escaped filename this script will not parse:"
    say "      ${line:0:70}"
    say "      Rename the file; evidence filenames should be boring."
    fail=1
    continue
  fi
  want="${line%% *}"
  path="${line#* }"
  path="${path# }"                    # sha256sum writes two spaces
  path="${path#./}"                   # manifest is generated from inside evidence/
  listed=$(( listed + 1 ))
  listed_paths+=("$path")

  if ! git cat-file -e "${COMMIT}:evidence/${path}" 2>/dev/null; then
    say "FAIL  listed evidence file is not in that commit: evidence/${path}"
    missing=$(( missing + 1 ))
    continue
  fi
  got="$(git show "${COMMIT}:evidence/${path}" | sha256sum | cut -d' ' -f1)"
  if [[ "$got" != "$want" ]]; then
    say "FAIL  evidence/${path} does not match the manifest"
    say "      manifest: ${want:0:16}…   commit: ${got:0:16}…"
    changed=$(( changed + 1 ))
  fi
done <<< "$manifest"

if (( missing || changed )); then
  fail=1
else
  say "ok    all ${listed} listed evidence file(s) match, read from the commit"
fi

# ------------------------------------------------- 3. evidence added later
#
# `sha256sum --check` can only check the files the manifest names. It is blind
# to files ADDED afterwards — so a candidate could commit better evidence after
# issue, link it from EVIDENCE.md, and still show a green verification. That is
# precisely what the manifest is claimed to prevent, so check it explicitly.
actual="$(git ls-tree -r --name-only "$COMMIT" -- evidence/ \
          | sed 's|^evidence/||' | grep -v '^manifest\.sha256$' || true)"
unlisted=""
while IFS= read -r f; do
  [[ -z "$f" ]] && continue
  found=0
  for p in ${listed_paths[@]+"${listed_paths[@]}"}; do
    [[ "$p" == "$f" ]] && { found=1; break; }
  done
  (( found )) || unlisted+="      evidence/${f}"$'\n'
done <<< "$actual"

if [[ -n "$unlisted" ]]; then
  say "FAIL  evidence present in that commit but NOT in the manifest:"
  printf '%s' "$unlisted"
  say "      Evidence added after the manifest was generated is evidence that"
  say "      was never assessed. Regenerate, re-issue, or remove it."
  fail=1
else
  say "ok    no unlisted evidence — the manifest covers everything in evidence/"
fi

# -------------------------------------------------------------- 4. manifest
ACTUAL="$(git show "${COMMIT}:evidence/manifest.sha256" | sha256sum | cut -d' ' -f1)"
if [[ -z "$EXPECTED_MANIFEST" ]]; then
  say ""
  say "NOT VERIFIED — no certificate hash was supplied, so nothing was checked"
  say "against a certificate. This commit's manifest hash is:"
  say ""
  say "      $ACTUAL"
  say ""
  say "Re-run with it as the second argument, or compare it to the certificate"
  say "by eye. Do not treat the checks above as a verified credential."
  exit 2
fi

if [[ "$ACTUAL" == "$EXPECTED_MANIFEST" ]]; then
  say "ok    manifest hash matches the certificate"
else
  say "FAIL  manifest hash does not match the certificate"
  say "      certificate: ${EXPECTED_MANIFEST:0:32}…"
  say "      commit:      ${ACTUAL:0:32}…"
  say "      The manifest itself was replaced. Every file above may verify"
  say "      against it and still not be what was assessed."
  fail=1
fi

say ""
if (( fail )); then
  say "NOT VERIFIED. Do not rely on this certificate."
  exit 1
fi
say "Verified: the evidence in commit ${COMMIT:0:12} is exactly what the"
say "certificate names, and nothing has been added, removed or altered."
say "This says nothing about the quality of the assessment itself."
