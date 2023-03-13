from pymake import EScope
from foo.make import foo_target
from make import project

# Create the target set for the library
target_set = project.create_target_set("BarTargetSet")

# Configure the Bar executable
bar_target = target_set.add_executable("bar")
bar_target.link_to(EScope.PRIVATE, foo_target)
bar_target.add_sources(EScope.PRIVATE, "bar.cpp")
bar_target.install()
