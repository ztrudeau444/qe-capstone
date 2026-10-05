# Language profiles

Each profile supplies three executable tasks — `build.sh`, `test.sh`,
`analyze.sh` — with the same contract regardless of language:

| Task | Must do | Must produce |
|---|---|---|
| `build.sh` | Resolve dependencies and compile | A runnable artifact |
| `test.sh` | Run unit + integration tests **with coverage** | A coverage report at the path in `quality/thresholds.yml` |
| `analyze.sh` | Run static analysis and upload results | A SonarQube Cloud project analysis |

Add a profile by creating a directory with those three scripts. Nothing in
`.github/workflows/` should need to change — if it does, the abstraction has
leaked and that is worth a note in your `docs/refactor-log.md`.

The supplied C++ profile is CMake + CTest + gcovr. That is a choice, not a
requirement — build systems vary more in C++ than anywhere else, and this is
simply the most conventional option available. On Bazel, Meson or a hand-written
Makefile you replace the same three scripts and nothing else moves, which is the
whole point of the contract.
