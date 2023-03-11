from pymake.model.targets.build.library_target import LibraryTarget
from pymake.visitors.targets.build.library_target_visitor import ILibraryTargetVisitor

class NullLibraryTargetVisitor(ILibraryTargetVisitor):
    """
    Represents a visitor that does nothing.
    """
    def visit(self, target: LibraryTarget) -> None:
        """
        Generates the CMake code for the target.
        @param target The target to generate CMake code for.
        """
        # Do nothing
        pass
