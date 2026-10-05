# Test Strategy

Week 2. Assessed at the Week 2 exit gate.

## Scope

| | |
|---|---|
| **System under test** | |
| **What is in scope** | |
| **What is deliberately out of scope, and why** | |

## The layers

| Layer | What it covers here | Roughly how many | Runs in |
|---|---|---|---|
| Unit | | | Test stage |
| Integration | | | Test stage |
| E2E | | | Test stage |
| Smoke | | | Smoke stage |

**Why this shape?** <Defend the proportions. A pyramid is the default, not a
law — if yours is not one, say why.>

## Traceability

Every criterion in `acceptance-criteria.md` covered at the layer named there.

## The Gherkin Decision

*Week 2 §2.9. The justification is assessed, not the decision. A well-reasoned
"no" scores higher than an unreasoned "yes".*

**The deciding question:** who, outside the engineering team, will read these
scenarios and be capable of telling you one is wrong?

| | |
|---|---|
| **Answer — a name, or "nobody"** | |
| **Decision** | Adopt / Do not adopt |

**Justification**

<One paragraph.>

**If adopting:** which layer, and how will you prevent the reuse-pressure
failure mode — the drift toward `When I click the "Submit" button`?

**If not adopting:** how do your acceptance criteria stay legible to anyone who
needs to read them?

## Test data

| | |
|---|---|
| **Where it comes from** | |
| **How it is isolated between runs** | |
| **Anything sensitive, and how it is handled** | |

## Flaky test policy

| | |
|---|---|
| **How a flake is identified** | |
| **What happens to it** (quarantine? delete? fix within N days?) | |
| **Who owns that decision** | |
