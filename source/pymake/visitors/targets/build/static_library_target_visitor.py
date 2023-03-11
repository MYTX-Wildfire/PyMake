from abc import ABC, abstractmethod
from pymake.model.targets.build.static_library_target import StaticLibraryTarget

class IStaticLibraryTargetVisitor(ABC):
    """
    Base type for classes that generate CMake code for a static library target.
    """
    @abstractmethod
    def visit(self, target: StaticLibraryTarget) -> None:
        """
        Generates the CMake code for the static library target.
        @param target The static library target to generate CMake code for.
        """
        raise NotImplementedError()
