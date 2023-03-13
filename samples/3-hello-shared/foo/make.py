from pymake import EScope
from make import project

# Create the target set for the library
target_set = project.create_target_set("FooTargetSet")

# Configure the Foo library
foo_target = target_set.add_shared_library("foo")
foo_target.add_include_directories(
    EScope.PRIVATE,
    "."
)
foo_target.add_include_directories(
    EScope.INTERFACE,
    ".."
)
foo_target.add_sources(
    EScope.PRIVATE,
    "foo.h",
    "foo.cpp"
)
foo_target.install()
