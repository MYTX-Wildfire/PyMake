from abc import ABC, abstractmethod
from pymake.model.pymake_project import PyMakeProject

class IProjectVisitor(ABC):
    """
    Base type for classes that generate CMake code for a project.
    """
    @abstractmethod
    def visit(self, project: PyMakeProject) -> None:
        """
        Generates the CMake code for the project.
        @param project The project to generate CMake code for.
        """
        raise NotImplementedError()
