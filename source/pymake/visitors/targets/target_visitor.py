from abc import ABC, abstractmethod
from pymake.model.targets.target import Target

class ITargetVisitor(ABC):
    """
    Base type for classes that generate CMake code for a target.
    """
    @abstractmethod
    def visit(self, target: Target) -> None:
        """
        Generates the CMake code for the target.
        @param target The target to generate CMake code for.
        """
        raise NotImplementedError()
