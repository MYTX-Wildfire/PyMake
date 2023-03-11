from abc import ABC, abstractmethod
from pymake.model.targets.imported.external_library_target import ExternalLibraryTarget

class IExternalLibraryTargetVisitor(ABC):
    """
    Base type for classes that generate CMake code for an external library target.
    """
    @abstractmethod
    def visit(self, target: ExternalLibraryTarget) -> None:
        """
        Generates the CMake code for the target.
        @param target The target to generate CMake code for.
        """
        raise NotImplementedError()
