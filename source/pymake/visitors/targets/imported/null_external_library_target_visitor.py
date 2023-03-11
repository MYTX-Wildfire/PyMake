from pymake.model.targets.imported.external_library_target import ExternalLibraryTarget
from pymake.visitors.targets.imported.external_library_target_visitor import IExternalLibraryTargetVisitor

class NullExternalLibraryTargetVisitor(IExternalLibraryTargetVisitor):
    """
    Represents a visitor that does nothing.
    """
    def visit(self, target: ExternalLibraryTarget) -> None:
        """
        Generates the CMake code for the target.
        @param target The target to generate CMake code for.
        """
        # Do nothing
        pass
