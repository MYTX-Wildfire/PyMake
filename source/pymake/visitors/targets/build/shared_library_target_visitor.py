from abc import ABC, abstractmethod
from pymake.model.targets.build.shared_library_target import SharedLibraryTarget

class ISharedLibraryTargetVisitor(ABC):
    """
    Base type for classes that generate CMake code for a shared library target.
    """
    @abstractmethod
    def visit(self, target: SharedLibraryTarget) -> None:
        """
        Generates the CMake code for the shared library target.
        @param target The shared library target to generate CMake code for.
        """
        raise NotImplementedError()
