from pymake.model.targets.docs.documentation_target import DocumentationTarget
from pymake.visitors.targets.docs.documentation_target_visitor import IDocumentationTargetVisitor

class NullDocumentationTargetVisitor(IDocumentationTargetVisitor):
    """
    Represents a visitor that does nothing.
    """
    def visit(self, target: DocumentationTarget) -> None:
        """
        Generates the CMake code for the target.
        @param target The target to generate CMake code for.
        """
        # Do nothing
        pass
