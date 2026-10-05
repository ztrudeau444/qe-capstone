# C++ profile

CMake + CTest + gcovr, chosen because they are the most conventional thing
available rather than the best thing available.

## What is here

| File | Why |
|---|---|
| `CMakeLists.txt` | The build. Coverage instrumentation is on for Debug |
| `build.sh` · `test.sh` · `analyze.sh` | The same three-verb contract every profile implements |
| `../../src/cpp/qe_test.h` | A 67-line assertion harness, so the starter runs before you have solved a dependency problem |

## The honest caveats

**The harness is not a test framework.** It has no fixtures, no parameterised
cases, no matchers, no mocking. **GoogleTest or Catch2 is the real answer** and
moving to one is a legitimate Week 2 exercise — the test names and assertions
survive, only the harness changes. If that swap turns out to be hard, your tests
were coupled to the harness, which is the lesson.

**Analyze costs more here than anywhere else.** SonarQube's C++ analyser cannot
infer how your code was compiled, so it needs a compilation database that the
other three profiles get for free from their build descriptors. `analyze.sh`
generates one with CMake; a build system that cannot emit
`compile_commands.json` will need the build-wrapper instead.

**gcov coverage is compiler-specific.** These scripts assume gcc or clang.
MSVC needs OpenCppCoverage and a different report path in
`quality/thresholds.yml`.

**If you use Bazel, Meson or plain Make**, replace these three scripts and leave
everything else alone. That is the point of the three-verb contract: the
pipeline never learns what build system you chose.
