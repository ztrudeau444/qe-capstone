# Framework layers

The structure the program argues for in Week 2 §3, present from Week 1 so you
never have to reorganise mid-course.

| Directory | Holds | Must not hold |
|---|---|---|
| `base/` | Drivers, hooks, setup and teardown, shared assertions | Anything that knows about a specific page or endpoint |
| `pages/` | Page objects and API clients — *where things are and how to act on them* | Assertions about business outcomes |
| `tests/` | Unit, integration, E2E and smoke tests — *what should be true* | Element selectors, URLs, waits |
| `utils/` | Waits, logging, data builders, helpers | Test logic |
| `config/` | Environment settings and threshold references | Secrets |

**The one rule that keeps this honest:** a selector never appears outside
`pages/`, and an assertion about behaviour never appears inside it. When you
find yourself breaking that rule, the fix is usually a missing method on a page
object — write it down in `docs/refactor-log.md` either way.

## Where each test type lives

```
src/tests/
 ├── unit/           fast, no I/O, no network       (Week 1)
 ├── integration/    database, queue, another service (Week 2)
 ├── e2e/            drives the running system      (Week 2)
 └── smoke/          two or three checks, under 2 min (Week 4)
```

Tag them so each pipeline stage can run one slice: JUnit `@Tag`, pytest markers,
xUnit `[Trait]`. A stage that runs the whole suite is a stage you will learn to
skip.
