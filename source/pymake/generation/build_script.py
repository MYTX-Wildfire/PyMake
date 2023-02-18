import os
from pathlib import Path
from pymake.helpers.caller_info import CallerInfo
from typing import List, NamedTuple

class GeneratedCode(NamedTuple):
    """
    Represents one or more lines of CMake code that was generated.
    """
    # The CMake code that was generated
    code: str

    # The caller info for the build script code that resulted in the CMake code
    #   getting generated
    caller_info: CallerInfo


class BuildScript:
    """
    Represents a CMakeLists.txt or .cmake file to be generated.
    """
    def __init__(self, filename: str, rel_path: str, root_path: str) -> None:
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

        # Lines to write into the target file
        self._lines: List[GeneratedCode] = []

    @property
    def target_path(self) -> str:
        """
        Returns the absolute path that the generated file should be written to.
        """
        return os.path.join(self._root_path, self._rel_path, self._filename)


    def append(self,
        cmake_code: str,
        caller_offset: int) -> None:
        """
        Adds a string containing CMake code to the script.
        This method will not append any characters to the provided CMake code.
        @param cmake_code CMake code to append.
        @param caller_offset Extra offset to apply to account for the stack
          frame of PyMake methods invoking this method when retrieving the stack
          frame from a build script.
        """
        self._lines.append(GeneratedCode(
            code=cmake_code,
            caller_info=CallerInfo(2 + caller_offset)
        ))

    def append_line(self,
        cmake_code: str,
        caller_offset: int) -> None:
        """
        Adds a string containing CMake code to the script.
        This method will append a newline character to the provided string.
        @param cmake_code CMake code to append.
        @param caller_offset Extra offset to apply to account for the stack
          frame of PyMake methods invoking this method when retrieving the stack
          frame from a build script.
        """
        self.append(cmake_code + '\n', caller_offset + 1)

    def generate_file_contents(self,
        source_tree_path: Path) -> str:
        """
        Generates a string containing the text to be written to the file.
        @path source_tree_path Absolute path to the source tree root.
        @returns A string containing the CMake build script code to write to the
          file.
        """
        contents = ""
        source_tree_path = source_tree_path.resolve()

        # Generate the file and add comments indicating where each line
        #   originated from
        for c in self._lines:
            file_path = c.caller_info.file_path
            line = c.caller_info.line_number

            # If possible, print the build script's path as a relative path
            try:
                build_script_path = Path(file_path).resolve()
                file_path = build_script_path.relative_to(source_tree_path)
            except ValueError:
                # The build script is not located in the source tree. Use the
                #   full path to the file instead.
                pass

            # If the file is in the source tree, write its relative path to
            #   the file instead of the full path
            contents += f"# {file_path}:{line}\n"
            contents += c.code

        return contents

