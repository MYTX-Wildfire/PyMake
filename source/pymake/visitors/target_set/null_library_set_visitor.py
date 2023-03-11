from pymake.model.target_sets.library_set import LibrarySet
from pymake.visitors.target_set.library_set_visitor import ILibrarySetVisitor

class NullLibrarySetVisitor(ILibrarySetVisitor):
    """
    Represents a visitor that does nothing.
    """
    def visit(self, library_set: LibrarySet) -> None:
        """
        Generates the CMake code for the library set.
        @param library_set The library set to generate CMake code for.
        """
        # Do nothing
        pass
