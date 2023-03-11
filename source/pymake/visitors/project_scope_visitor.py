from abc import ABC, abstractmethod
from pymake.model.project_scope import ProjectScope

class IProjectScopeVisitor(ABC):
    """
    Base type for classes that generate CMake code for a project scope.
    """
    @abstractmethod
    def visit(self, project_scope: ProjectScope) -> None:
        """
        Generates the CMake code for the project scope.
        @param project_scope The project scope to generate CMake code for.
        """
        raise NotImplementedError()
