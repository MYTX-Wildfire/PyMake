from pymake.model.targets.build.build_target import BuildTarget
from pymake.visitors.targets.build.build_target_visitor import IBuildTargetVisitor

class NullBuildTargetVisitor(IBuildTargetVisitor):
    """
    Represents a visitor that does nothing.
    """
    def visit(self, target: BuildTarget) -> None:
        """
        Generates the CMake code for the target.
        @param target The target to generate CMake code for.
        """
        # Do nothing
        pass
