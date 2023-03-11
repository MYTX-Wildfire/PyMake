from abc import ABC, abstractmethod
from pymake.model.targets.build.executable_target import ExecutableTarget

class IExecutableTargetVisitor(ABC):
    """
    Base type for classes that generate CMake code for an executable target.
    """
    @abstractmethod
    def visit(self, target: ExecutableTarget) -> None:
        """
        Generates the CMake code for the executable target.
        @param target The target to generate CMake code for.
        """
        raise NotImplementedError()
