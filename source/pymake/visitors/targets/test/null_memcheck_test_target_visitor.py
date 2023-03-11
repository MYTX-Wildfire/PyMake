from pymake.model.targets.test.memcheck_test_target import MemcheckTestTarget
from pymake.visitors.targets.test.memcheck_test_target_visitor import IMemcheckTestTargetVisitor

class NullMemcheckTestTargetVisitor(IMemcheckTestTargetVisitor):
    """
    Represents a visitor that does nothing.
    """
    def visit(self, target: MemcheckTestTarget) -> None:
        """
        Generates the CMake code for the target.
        @param target The target to generate CMake code for.
        """
        # Do nothing
        pass
