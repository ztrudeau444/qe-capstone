## What changed

<!-- One sentence. If you need three, this is probably two pull requests. -->

## Which acceptance criterion does this serve?

<!-- Reference the ID from docs/acceptance-criteria.md. "None" is a valid
     answer for a refactor — say so. -->

## Test evidence

- [ ] Unit tests added or updated
- [ ] Integration test added, or a note on why the unit layer is sufficient
- [ ] Coverage did not fall
- [ ] Pipeline green

## Quality gates

- [ ] No new code smells
- [ ] No new security findings, or the finding is suppressed in `quality/security/.snyk` (which is the file Snyk actually reads) with an owner and an expiry, and recorded in `quality/thresholds.yml` under `security.accepted`
- [ ] Thresholds unchanged, or the change is justified in `docs/refactor-log.md`

## Risk

<!-- What could this break that the pipeline would not catch? If the honest
     answer is "nothing", say that — but say it deliberately. -->
