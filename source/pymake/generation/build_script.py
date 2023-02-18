from pathlib import Path
from pymake.generation.code_generator import ICodeGenerator
from typing import List

class BuildScript:
    """
    Represents a CMakeLists.txt or .cmake file to be generated.
    """
    def __init__(self, filename: str, rel_path: Path, root_path: Path) -> None:
        """
        Initializes the object.
        @param filename Name of the file that should be generated. Should either
          be 'CMakeLists.txt' or a file name ending in '.cmake'.
        @param rel_path Path relative to the root folder used for the generated
          build scripts.
        @param root_path Absolute path to the root folder where generated build
          scripts should be placed.
        """
        self._filename = filename
        self._rel_path = rel_path
        self._root_path = root_path
        self._target_path = Path.joinpath(
            self._root_path,
            self._rel_path,
            self._filename
        ).absolute().resolve()

        # Generators to invoke when generating the build script
        self._generators: List[ICodeGenerator] = []

    @property
    def target_path(self) -> Path:
        """
        Returns the absolute path that the generated file should be written to.
        """
        return self._target_path

    def add_generator(self, generator: ICodeGenerator) -> None:
        """
        Adds a generator to invoke to create CMake code for the generated file.
        @param generator Code generator to invoke when adding code into the
          generated file.
        """
        self._generators.append(generator)

    def generate_file_contents(self,
        source_tree_path: Path) -> str:
        """
        Generates a string containing the text to be written to the file.
        @path source_tree_path Absolute path to the source tree root.
        @returns A string containing the CMake build script code to write to the
          file.
        """
        source_tree_path = source_tree_path.resolve()
        return "\n\n".join([
            g.generate(source_tree_path) for g in self._generators
        ])
