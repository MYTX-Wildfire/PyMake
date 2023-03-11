from pymake.model.targets.target import Target
from pymake.visitors.targets.target_visitor import ITargetVisitor

class NullTargetVisitor(ITargetVisitor):
    """
    Represents a visitor that does nothing.
    """
    def visit(self, target: Target) -> None:
        """
        Generates the CMake code for the target.
        @param target The target to generate CMake code for.
        """
        # Do nothing
        pass
