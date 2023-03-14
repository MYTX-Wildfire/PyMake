from pymake import ESanitizerFlags, EScope
from make import project

# Create the target set for the library
foo_target_set = project.create_target_set("FooTargetSet")

# Configure the Foo library
foo_target = foo_target_set.add_static_library("foo")
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

# Build sanitized versions of the library
foo_asan_target = foo_target_set.add_sanitized_target(
    "foo_asan",
    ESanitizerFlags.ADDRESS,
    foo_target
)
