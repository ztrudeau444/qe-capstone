#pragma once
//
// A 67-line assertion harness, so the starter runs before you have solved a
// dependency problem.
//
// GoogleTest and Catch2 are both better than this and you should move to one of
// them — see Appendix C. What they add is fixtures, parameterised cases,
// matchers, death tests and mocking. What they cost is a dependency you have to
// fetch before anything runs at all, which is the wrong trade for Week 0.
//
// Swapping this out is a legitimate Week 2 framework-architecture exercise: the
// test names and the assertions stay, only the harness changes. If that swap is
// hard, your tests were coupled to the harness, which is the lesson.
#include <cstdio>
#include <cstdlib>
#include <string>
#include <vector>
#include <functional>

namespace qe {

struct Case { std::string name; std::function<void()> fn; };

inline std::vector<Case>& registry() {
  static std::vector<Case> cases;
  return cases;
}

inline int& failures() { static int f = 0; return f; }

struct Register {
  Register(const std::string& name, std::function<void()> fn) {
    registry().push_back({name, std::move(fn)});
  }
};

inline void check(bool ok, const char* expr, const char* file, int line) {
  if (!ok) {
    std::printf("    FAILED  %s\n            at %s:%d\n", expr, file, line);
    ++failures();
  }
}

inline int run_all() {
  int failed_cases = 0;
  for (auto& c : registry()) {
    int before = failures();
    c.fn();
    bool ok = failures() == before;
    std::printf("  %s  %s\n", ok ? "PASS" : "FAIL", c.name.c_str());
    if (!ok) ++failed_cases;
  }
  std::printf("\n%zu case(s), %d failed\n", registry().size(), failed_cases);
  return failed_cases == 0 ? 0 : 1;
}

}  // namespace qe

#define QE_TEST(name)                                                        \
  static void name();                                                        \
  static ::qe::Register reg_##name(#name, name);                             \
  static void name()

#define QE_ASSERT(expr) ::qe::check((expr), #expr, __FILE__, __LINE__)
#define QE_ASSERT_EQ(a, b) ::qe::check((a) == (b), #a " == " #b, __FILE__, __LINE__)

#define QE_MAIN() int main() { return ::qe::run_all(); }
