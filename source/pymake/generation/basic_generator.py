from pathlib import Path
from pymake.generation.code_generator import ICodeGenerator
from pymake.helpers.caller_info import CallerInfo
from pymake.helpers.path_statics import shorten_path

class BasicGenerator(ICodeGenerator):
    """
    Generator for CMake code that require minimal annotations.
    This generator can be used when the only extra annotation that should be
      the build script and line number that the line of code came from. If
      additional elements of the generated code should be annotated, use a
      different code generator implementation.
    """

    def __init__(self, code: str, caller_offset: int):
        """
        Initializes the generator.
        @param code CMake code to return when the generator is invoked.
        @param caller_offset Offset in number of stack frames to apply to get
          the stack frame of the build script using PyMake. This value should
          only account for the PyMake stack frames between this method and the
          external build script.
        """
        self._code = code
        # Add 1 to account for this constructor's stack frame
        self._caller_info = CallerInfo(caller_offset + 1)

    def generate(self, source_tree_path: Path) -> str:
        """
        Generates the CMake code to insert into a build script.
        @param source_tree_path Path to the root of the source tree for the
          PyMake-based project.
        @returns The CMake code to insert into a build script. This string may
          consist of multiple lines.
        """
        # Get the path that should be written to the generated file
        source_path = shorten_path(
            self._caller_info.file_path,
            source_tree_path
        )

        # Add the comment indicating where the line originated from in the
        #   PyMake scripts
        generated_code = f"# {source_path}:{self._caller_info.line_number}\n"
        generated_code += self._code
        return generated_code

