from pymake.model.targets.test.valgrind_test_target import ValgrindTestTarget
from pymake.visitors.targets.test.valgrind_test_target_visitor import IValgrindTestTargetVisitor

class NullValgrindTestTargetVisitor(IValgrindTestTargetVisitor):
    """
    Base type for classes that generate CMake code for a ValgrindTest target.
    """
    def visit(self, target: ValgrindTestTarget) -> None:
        """
        Generates the CMake code for the ValgrindTest target.
        @param target The ValgrindTest target to generate CMake code for.
        """
        # Do nothing
        pass
