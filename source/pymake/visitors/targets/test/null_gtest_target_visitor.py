from pymake.model.targets.test.gtest_target import GTestTarget
from pymake.visitors.targets.test.gtest_target_visitor import IGTestTargetVisitor

class NullGTestTargetVisitor(IGTestTargetVisitor):
    """
    Represents a visitor that does nothing.
    """
    def visit(self, target: GTestTarget) -> None:
        """
        Generates the CMake code for the target.
        @param target The target to generate CMake code for.
        """
        # Do nothing
        pass
