from pymake.model.targets.test.test_target import TestTarget
from pymake.visitors.targets.test.test_target_visitor import ITestTargetVisitor

class NullTestTargetVisitor(ITestTargetVisitor):
    """
    Represents a visitor that does nothing.
    """
    def visit(self, target: TestTarget) -> None:
        """
        Generates the CMake code for the target.
        @param target The target to generate CMake code for.
        """
        # Do nothing
        pass
