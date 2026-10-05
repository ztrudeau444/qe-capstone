cmake_minimum_required(VERSION 3.16)
project(qe_starter CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Coverage instrumentation, on for the Debug build the pipeline uses. gcov needs
# both flags: --coverage on compile AND on link, and forgetting the second is
# the classic reason a C++ coverage report comes back empty.
option(ENABLE_COVERAGE "Build with gcov instrumentation" ON)
if(ENABLE_COVERAGE)
  add_compile_options(--coverage -O0 -g)
  add_link_options(--coverage)
endif()

include(CTest)
enable_testing()

# Your production code. Add sources here as you write them.
add_library(sut
  ${CMAKE_CURRENT_SOURCE_DIR}/../../src/cpp/discount.cpp
)
target_include_directories(sut PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/../../src/cpp)

# One test binary per suite keeps failures attributable. CTest runs each and
# reports them separately.
add_executable(unit_tests
  ${CMAKE_CURRENT_SOURCE_DIR}/../../src/tests/unit/cpp/test_discount.cpp
)
target_link_libraries(unit_tests PRIVATE sut)
add_test(NAME unit COMMAND unit_tests)
