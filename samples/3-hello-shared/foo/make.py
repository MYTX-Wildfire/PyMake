from pymake import EScope
from make import project

# Configure the Foo library
foo_target = project.add_shared_library("foo")
foo_target.add_include_directories(".")
foo_target.add_include_directories("..", scope=EScope.INTERFACE)
foo_target.add_sources(["foo.h", "foo.cpp"])
foo_target.install()
