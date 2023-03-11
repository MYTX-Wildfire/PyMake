from pymake.model.targets.build.shared_library_target import SharedLibraryTarget
from pymake.visitors.targets.build.shared_library_target_visitor import ISharedLibraryTargetVisitor

class NullSharedLibraryTargetVisitor(ISharedLibraryTargetVisitor):
    """
    Represents a visitor that does nothing.
    """
    def visit(self, target: SharedLibraryTarget) -> None:
        """
        Generates the CMake code for the target.
        @param target The target to generate CMake code for.
        """
        # Do nothing
        pass
