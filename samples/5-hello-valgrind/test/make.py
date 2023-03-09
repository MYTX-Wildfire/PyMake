from foo.make import foo_target
from make import project

# Configure the test executable
test_target = project.add_executable("foo_tests")
test_target.link_to_target(foo_target)
test_target.add_sources("test.cpp")
test_target.link_to_library("gtest", is_static=True)
test_target.link_to_library("gtest_main", is_static=True)
test_target.mark_is_test_target(
    add_valgrind_target=True,
    add_helgrind_target=True,
    add_drd_target=True
)
test_target.install()
