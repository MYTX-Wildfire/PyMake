from abc import ABC, abstractmethod
from pathlib import Path

class ICodeGenerator(ABC):
    """
    Base interface for classes that generate CMake code.
    """
    @abstractmethod
    def generate(self, source_tree_path: Path) -> str:
        """
        Generates the CMake code to insert into a build script.
        @note Newline characters will be added between each generator's
          string. Generators should not append additional newline characters at
          the end of their strings unless the intent is to have multiple empty
          lines in the generated code.
        @param source_tree_path Path to the root of the source tree for the
          PyMake-based project. This path will be an absolute path that has
          already been resolved.
        @returns The CMake code to insert into a build script. This string may
          consist of multiple lines.
        """
        raise NotImplementedError()
