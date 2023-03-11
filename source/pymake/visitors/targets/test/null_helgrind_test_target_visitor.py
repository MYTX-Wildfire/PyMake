from pymake.model.targets.test.helgrind_test_target import HelgrindTestTarget
from pymake.visitors.targets.test.helgrind_test_target_visitor import IHelgrindTestTargetVisitor

class NullHelgrindTestTargetVisitor(IHelgrindTestTargetVisitor):
    """
    Represents a visitor that does nothing.
    """
    def visit(self, target: HelgrindTestTarget) -> None:
        """
        Generates the CMake code for the target.
        @param target The target to generate CMake code for.
        """
        # Do nothing
        pass
