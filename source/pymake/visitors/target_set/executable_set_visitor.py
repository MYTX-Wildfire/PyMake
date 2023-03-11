from abc import ABC, abstractmethod
from pymake.model.target_sets.executable_set import ExecutableSet

class IExecutableSetVisitor(ABC):
    """
    Base type for classes that generate CMake code for an executable set.
    """
    @abstractmethod
    def visit(self, executable_set: ExecutableSet) -> None:
        """
        Generates the CMake code for the executable set.
        @param executable_set The executable set to generate CMake code for.
        """
        raise NotImplementedError()
