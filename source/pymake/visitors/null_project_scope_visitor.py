from pymake.model.project_scope import ProjectScope
from pymake.visitors.project_scope_visitor import IProjectScopeVisitor

class NullProjectScopeVisitor(IProjectScopeVisitor):
    """
    Represents a visitor that does nothing.
    """
    def visit(self, project_scope: ProjectScope) -> None:
        """
        Generates the CMake code for the project scope.
        @param project_scope The project scope to generate CMake code for.
        """
        # Do nothing
        pass
