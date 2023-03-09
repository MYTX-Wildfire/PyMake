from foo.make import foo_target
from make import project

# Configure the test executable
test_target = project.add_gtest_target("foo_tests")
test_target.link_to_target(foo_target)
test_target.add_sources("test.cpp")
test_target.link_to_library("gtest", is_static=True)
test_target.link_to_library("gtest_main", is_static=True)
test_target.install()
