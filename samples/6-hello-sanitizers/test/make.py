from foo.make import foo_target_set, foo_target
from make import gtest_target, gtest_main_target
from pymake import ESanitizerFlags, EScope, ETestFlags

# Add the test executable as a target in the Foo target set
test_target = foo_target_set.add_gtest_executable(
    "foo_tests",
    ETestFlags.UNIT
)
test_target.add_sources(EScope.PRIVATE, "test.cpp")
test_target.link_to(
    EScope.PRIVATE,
    foo_target,
    gtest_target,
    gtest_main_target
)
test_target.install()

# Add the asan-enabled test executable
test_asan_target = foo_target_set.add_sanitized_target(
    "foo_tests_asan",
    ESanitizerFlags.ADDRESS,
    test_target
)
test_asan_target.install()
