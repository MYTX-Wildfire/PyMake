from pymake.model.pymake_project import PyMakeProject
from pymake.visitors.project_visitor import IProjectVisitor

class NullProjectVisitor(IProjectVisitor):
    """
    Represents a visitor that does nothing.
    """
    def visit(self, project: PyMakeProject) -> None:
        """
        Generates the CMake code for the project.
        @param project The project to generate CMake code for.
        """
        # Do nothing
        pass
