from abc import ABC, abstractmethod
from pymake.model.target_sets.library_set import LibrarySet

class ILibrarySetVisitor(ABC):
    """
    Base type for classes that generate CMake code for a library set.
    """
    @abstractmethod
    def visit(self, library_set: LibrarySet) -> None:
        """
        Generates the CMake code for the library set.
        @param library_set The library set to generate CMake code for.
        """
        raise NotImplementedError()
