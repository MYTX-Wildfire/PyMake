from foo.make import foo_target
from make import project

# Configure the Bar executable
bar_target = project.add_executable("bar")
bar_target.link_to_target(foo_target)
bar_target.add_sources("bar.cpp")
bar_target.install()
