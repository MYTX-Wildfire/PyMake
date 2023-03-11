from pymake.model.targets.test.drd_test_target import DrdTestTarget
from pymake.visitors.targets.test.drd_test_target_visitor import IDrdTestTargetVisitor

class NullDrdTestTargetVisitor(IDrdTestTargetVisitor):
    """
    Represents a visitor that does nothing.
    """
    def visit(self, target: DrdTestTarget) -> None:
        """
        Generates the CMake code for the target.
        @param target The target to generate CMake code for.
        """
        # Do nothing
        pass
