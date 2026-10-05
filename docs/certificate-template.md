# Certificate of Completion — template

Fill every field. A field you cannot fill honestly is a field to delete, not to
guess at.

---

## Quality Engineering Practitioner

**Project Work Automation, Clean Code & Software Quality Engineering**
Canadian Edition 2025 · four-week program

---

**Awarded to:** _______________________________________________

**Certificate ID:** QE-2025-____________

**Date of assessment:** ______________________

**Assessed by:** ____________________________ , ____________________________
                 (name)                          (role)

---

### What this certifies

This person built and defended a working eight-stage quality-engineering
pipeline on a System Under Test of their own choosing, over four weeks, and the
evidence is public and verifiable at the commit named below.

**Repository:** ____________________________________________________

**Commit:** ________________________________________________________
            (full 40-character SHA — a branch name is not a commit)

**Evidence manifest (SHA-256 of `evidence/manifest.sha256`):**

`_____________________________________________________________`

### Gates at assessment

| Gate | Threshold | Result | Met |
|---|---|---|---|
| Line coverage | ≥ 80% | ____ % | ☐ |
| Branch coverage | ≥ 60% | ____ % | ☐ |
| Maintainability | Grade A | ____ | ☐ |
| p95 latency under load | ≤ 500 ms | ____ ms | ☐ |
| Error rate under load | < 1% | ____ % | ☐ |
| Critical CVEs | 0 | ____ | ☐ |
| High CVEs | 0 | ____ | ☐ |
| Accessibility | ≥ 95 | ____ | ☐ |
| Functional criteria covered | 100% | ____ % | ☐ |
| Full pipeline green, one commit | 8 of 8 | ____ of 8 | ☐ |

**Gates not met, and why:**

_____________________________________________________________________

_____________________________________________________________________

> A blank line here on a certificate where every box is ticked is fine and
> normal. A blank line where a box is unticked is a certificate that has been
> tidied, and any experienced reader will treat the whole document accordingly.

### What this does not certify

- It is **not** a statement about general engineering ability.
- It is **not** a prediction of performance on a different codebase.
- It has **no expiry**, and therefore makes no claim about current skill. Read the assessment date.
- Verification below proves the artifact is real and unaltered. It does **not** prove the assessment was rigorous — that rests on the named assessor.

### How to verify this certificate

Anyone, without contacting the candidate or the issuer:

```bash
git clone <repository> && cd <repository>
./scripts/verify-certificate.sh <commit> <manifest-hash>
```

That is the whole procedure. The script reads every file **out of the named
commit** rather than off your disk, so nothing about your checkout can affect
the answer. It confirms the commit is reachable from a branch or tag, hashes
each listed evidence file as that commit stored it, checks that no evidence was
added after the manifest was generated, and compares the manifest's own hash to
the one printed above.

By hand, if you would rather not run someone else's script:

```bash
git clone <repository> && cd <repository>
git show <commit>:evidence/manifest.sha256 | sha256sum   # must equal the hash above
git checkout <commit>
( cd evidence && sha256sum --check manifest.sha256 )
```

**Both halves are needed.** `--check` on its own proves only that the files
match a manifest the candidate wrote; comparing the manifest's own hash to this
certificate is what proves the manifest is the one that was assessed. A clean
`--check` against a regenerated manifest means nothing.

Then open `EVIDENCE.md` and follow any claim to its artifact. A link that does
not resolve is a finding.

The issuer's published criteria are at: ________________________________

---

*Issued under an **instructor-attested** model: a named assessor examined this
evidence on the date above, against the published criteria linked above. No
accrediting organisation stands behind it, and none is implied.*

*If your delivery differs, this line and the assessor block are the only two
places to change — see Week 5 §5.1. Use **self-attested** if there was no
assessor, and **organisation-attested** only if a body with real governance,
consistent marking and an appeals process is genuinely behind it. Claiming the
third while operating the first is the one thing here a reviewer can catch you
on.*
