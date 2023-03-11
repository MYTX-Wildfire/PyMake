from abc import ABC, abstractmethod
from pymake.model.targets.build.build_target import BuildTarget

class IBuildTargetVisitor(ABC):
    """
    Base type for classes that generate CMake code for a build target.
    """
    @abstractmethod
    def visit(self, target: BuildTarget) -> None:
        """
        Generates the CMake code for the target.
        @param target The target to generate CMake code for.
        """
        raise NotImplementedError()
