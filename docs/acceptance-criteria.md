# Acceptance Criteria

Week 1. At least eight, at least three in full three-clause form.

**Three-clause prose, not Gherkin.** Week 1 deliberately has no specification
DSL — the tooling decision comes in Week 2 §2.9 once you have E2E automation
for it to wrap. Right now you are learning to *state* a behaviour precisely.

## The form

> **Given** some starting state
> **When** something happens
> **Then** an observable outcome, and nothing else changed

The last clause is the one people skip and the one that catches defects.

## Criteria

### AC-01 — <short name>

**Given** …
**When** …
**Then** …

| | |
|---|---|
| **Type** | Functional / Non-functional |
| **Test layer** | Unit / Integration / E2E |
| **Why that layer** | <one sentence — this is assessed> |
| **Test** | `<path::testName>` |
| **Status** | Not started / Red / Green |

### AC-02 — <short name>

**Given** …
**When** …
**Then** …

| | |
|---|---|
| **Type** | |
| **Test layer** | |
| **Why that layer** | |
| **Test** | |
| **Status** | |

<!-- Repeat to AC-08 or beyond. -->

## Traceability

Every functional criterion must reach 100% coverage by the Week 4 exit gate.

| ID | Criterion | Layer | Test | Green |
|---|---|---|---|---|
| AC-01 | | | | ☐ |
| AC-02 | | | | ☐ |
| AC-03 | | | | ☐ |
| AC-04 | | | | ☐ |
| AC-05 | | | | ☐ |
| AC-06 | | | | ☐ |
| AC-07 | | | | ☐ |
| AC-08 | | | | ☐ |
