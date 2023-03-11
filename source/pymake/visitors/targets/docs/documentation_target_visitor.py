from abc import ABC, abstractmethod
from pymake.model.targets.docs.documentation_target import DocumentationTarget

class IDocumentationTargetVisitor(ABC):
    """
    Base type for classes that generate CMake code for a documentation target.
    """
    @abstractmethod
    def visit(self, target: DocumentationTarget) -> None:
        """
        Generates the CMake code for the documentation target.
        @param target The documentation target to generate CMake code for.
        """
        raise NotImplementedError()
