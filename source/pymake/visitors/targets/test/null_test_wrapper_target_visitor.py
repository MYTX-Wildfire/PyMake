from pymake.model.targets.test.test_wrapper_target import TestWrapperTarget
from pymake.visitors.targets.test.test_wrapper_target_visitor import ITestWrapperTargetVisitor

class NullTestWrapperTargetVisitor(ITestWrapperTargetVisitor):
    """
    Represents a visitor that does nothing.
    """
    def visit(self, target: TestWrapperTarget) -> None:
        """
        Generates the CMake code for the target.
        @param target The target to generate CMake code for.
        """
        # Do nothing
        pass
