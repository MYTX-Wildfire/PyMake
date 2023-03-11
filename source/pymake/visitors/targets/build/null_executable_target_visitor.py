from pymake.model.targets.build.executable_target import ExecutableTarget
from pymake.visitors.targets.build.executable_target_visitor import IExecutableTargetVisitor

class NullExecutableTargetVisitor(IExecutableTargetVisitor):
    """
    Represents a visitor that does nothing.
    """
    def visit(self, target: ExecutableTarget) -> None:
        """
        Generates the CMake code for the target.
        @param target The target to generate CMake code for.
        """
        # Do nothing
        pass
