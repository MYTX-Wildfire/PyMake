from abc import ABC, abstractmethod
from pathlib import Path

class ICodeGenerator(ABC):
    """
    Base interface for classes that generate CMake code.
    """
    @staticmethod
    def shorten_path(
        target_path: str,
        source_tree_path: Path) -> str:
        """
        Conditionally shortens the target path if it's in the source tree.
        This method is used to print more concise paths when writing source
          map style information to the generated CMake file. If the target
          path is within the source tree, the relative path from the source
          tree root will be returned instead of the full target path.
        @param target_path Absolute path to conditionally shorten.
        @param source_tree_path Absolute path to the root of the source tree.
          Should not contain any symlinks.
        @returns The target path as a path relative to the source tree path if
          the target path is in the source tree. If the target path is outside
          the source tree, returns the target path as-is.
        """
        try:
            path = Path(target_path).resolve()
            return str(path.relative_to(source_tree_path))
        except ValueError:
            # The build script is not located in the source tree. Use the
            #   full path to the file instead.
            return target_path

    @abstractmethod
    def generate(self, source_tree_path: Path) -> str:
        """
        Generates the CMake code to insert into a build script.
        @note A newline character will be added between each generator's
          string. Generators should not append a newline character at the end
          of their strings unless the intent is to have multiple empty lines
          in the generated code.
        @param source_tree_path Path to the root of the source tree for the
          PyMake-based project. This path will be an absolute path that has
          already been resolved.
        @returns The CMake code to insert into a build script. This string may
          consist of multiple lines.
        """
        raise NotImplementedError()
