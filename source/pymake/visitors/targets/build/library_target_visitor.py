from abc import ABC, abstractmethod
from pymake.model.targets.build.library_target import LibraryTarget

class ILibraryTargetVisitor(ABC):
    """
    Base type for classes that generate CMake code for a library target.
    """
    @abstractmethod
    def visit(self, target: LibraryTarget) -> None:
        """
        Generates the CMake code for the target.
        @param target The target to generate CMake code for.
        """
        raise NotImplementedError()
