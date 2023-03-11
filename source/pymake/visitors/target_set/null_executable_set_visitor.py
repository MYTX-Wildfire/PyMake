from pymake.model.target_sets.executable_set import ExecutableSet
from pymake.visitors.target_set.executable_set_visitor import IExecutableSetVisitor

class NullExecutableSetVisitor(IExecutableSetVisitor):
    """
    Represents a visitor that does nothing.
    """
    def visit(self, executable_set: ExecutableSet) -> None:
        """
        Generates the CMake code for the executable set.
        @param executable_set The executable set to generate CMake code for.
        """
        # Do nothing
        pass
