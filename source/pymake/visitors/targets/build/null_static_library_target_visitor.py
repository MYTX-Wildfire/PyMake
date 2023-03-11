from pymake.model.targets.build.static_library_target import StaticLibraryTarget
from pymake.visitors.targets.build.static_library_target_visitor import IStaticLibraryTargetVisitor

class NullStaticLibraryTargetVisitor(IStaticLibraryTargetVisitor):
    """
    Represents a visitor that does nothing.
    """
    def visit(self, target: StaticLibraryTarget) -> None:
        """
        Generates the CMake code for the target.
        @param target The target to generate CMake code for.
        """
        # Do nothing
        pass
