from pymake.model.targets.imported.imported_target import ImportedTarget
from pymake.visitors.targets.imported.imported_target_visitor import IImportedTargetVisitor

class NullImportedTargetVisitor(IImportedTargetVisitor):
    """
    Represents a visitor that does nothing.
    """
    def visit(self, target: ImportedTarget) -> None:
        """
        Generates the CMake code for the target.
        @param target The target to generate CMake code for.
        """
        # Do nothing
        pass
