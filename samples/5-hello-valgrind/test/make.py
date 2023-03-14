from foo.make import foo_target_set, foo_target
from make import gtest_target, gtest_main_target
from pymake import EScope, ETestFlags

# Add the gtest executable
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

# Add the three Valgrind test targets
drd_test_target = foo_target_set.add_drd_target(
    "foo_drd",
    test_target
)
helgrind_test_target = foo_target_set.add_helgrind_target(
    "foo_helgrind",
    test_target
)
memcheck_test_target = foo_target_set.add_memcheck_target(
    "foo_memcheck",
    test_target
)
