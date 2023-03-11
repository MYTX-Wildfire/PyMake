from abc import ABC, abstractmethod
from pymake.model.targets.docs.doxygen_target import DoxygenTarget

class IDoxygenTargetVisitor(ABC):
    """
    Base type for classes that generate CMake code for a Doxygen target.
    """
    @abstractmethod
    def visit(self, target: DoxygenTarget) -> None:
        """
        Generates the CMake code for the Doxygen target.
        @param target The Doxygen target to generate CMake code for.
        """
        raise NotImplementedError()
