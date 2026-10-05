# Framework Architecture

Week 2. This becomes the architecture slide in your Week 4 defence, so draw it
once and keep it current.

## Layers

```
src/
 ├── base/      <what you put here>
 ├── pages/     <…>
 ├── utils/     <…>
 ├── config/    <…>
 └── tests/     <…>
```

## The dependency rule

<State which direction dependencies flow and what is not allowed to import
what. Then say how you would notice if someone broke it — a lint rule, a
review checklist, or honestly, nothing yet.>

## Patterns used

| Pattern | Where | Why here rather than the simpler thing |
|---|---|---|
| | | |

*The third column is the one that gets marked. A pattern applied without a
reason is a Week 3 maintenance problem.*

## What this design makes hard

<Every structure trades something away. Name what yours makes harder — the
honesty is assessed, and reviewers probe designs presented as costless.>

## Traceability to Week 1

<Which SOLID argument from your Week 1 refactor produced which layer here.
This is the hand-off the program is built on — make it explicit.>
