from abc import ABC, abstractmethod
from pymake.model.targets.imported.imported_target import ImportedTarget

class IImportedTargetVisitor(ABC):
    """
    Base type for classes that generate CMake code for an imported target.
    """
    @abstractmethod
    def visit(self, target: ImportedTarget) -> None:
        """
        Generates the CMake code for the target.
        @param target The target to generate CMake code for.
        """
        raise NotImplementedError()
