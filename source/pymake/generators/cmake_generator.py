from pathlib import Path
from pymake.generators.cmake_method_builder import CMakeMethodBuilder
from pymake.generators.text_generator import TextGenerator
from pymake.tracing.caller_info_formatter import ICallerInfoFormatter

class CMakeGenerator:
    """
    Generator used to generate CMake files.
    """
    def __init__(self,
    	formatter: ICallerInfoFormatter,
        use_spaces: bool = False,
        tab_size: int = 4):
        """
        Initializes the generator.
        @param formatter Formatter used to format tracing information.
        @param use_spaces Whether spaces should be used in the generated string.
        @param tab_size Only used if `use_spaces` is true. Determines the number
          of spaces inserted for each indentation level.
        """
        self._text_generator = TextGenerator(use_spaces, tab_size)
        self._formatter = formatter


    def generate(self) -> str:
        """
        Gets the contents of the generated CMake file.
        @returns The contents of the generated CMake file.
        """
        return self._text_generator.text


    def open_method_block(self, method_name: str) -> CMakeMethodBuilder:
        """
        Opens a method block.
        @param method_name Name of the method.
        @returns A builder used to generate the method.
        """
        return CMakeMethodBuilder(
            self._formatter,
            self._text_generator,
            method_name
        )


    def write_file(self, output_path: str | Path) -> None:
        """
        Writes the generated CMake file to the specified path.
        @param output_path Path to write the generated CMake file to.
        """
        with open(output_path, "w") as f:
            f.write(self.generate())
