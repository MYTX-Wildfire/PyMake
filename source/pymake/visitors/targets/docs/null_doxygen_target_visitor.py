from pymake.model.targets.docs.doxygen_target import DoxygenTarget
from pymake.visitors.targets.docs.doxygen_target_visitor import IDoxygenTargetVisitor

class NullDoxygenTargetVisitor(IDoxygenTargetVisitor):
    """
    Represents a visitor that does nothing.
    """
    def visit(self, target: DoxygenTarget) -> None:
        """
        Generates the CMake code for the target.
        @param target The target to generate CMake code for.
        """
        # Do nothing
        pass
