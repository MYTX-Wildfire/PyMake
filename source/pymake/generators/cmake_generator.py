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
        self._use_spaces = use_spaces
        self._tab_size = tab_size
        self._formatter = formatter


    @property
    def formatter(self) -> ICallerInfoFormatter:
        """
        Gets the formatter used to format tracing information.
        """
        return self._formatter


    @property
    def use_spaces(self) -> bool:
        """
        Gets whether spaces should be used in the generated string.
        """
        return self._use_spaces


    @property
    def tab_size(self) -> int:
        """
        Gets the number of spaces inserted for each indentation level.
        """
        return self._tab_size


    def close_if_block(self) -> None:
        """
        Closes an if block.
        """
        self.decrease_indentation_level()
        self._text_generator.append_line("endif()")
        self._text_generator.append_line()


    def generate(self) -> str:
        """
        Gets the contents of the generated CMake file.
        @returns The contents of the generated CMake file.
        """
        return self._text_generator.text


    def decrease_indentation_level(self) -> None:
        """
        Decreases the indentation level by one.
        """
        self._text_generator.decrease_indentation_level()


    def increase_indentation_level(self) -> None:
        """
        Increases the indentation level by one.
        """
        self._text_generator.increase_indentation_level()


    def open_if_block(self, if_condition: str) -> None:
        """
        Opens an if block.
        @param if_condition The condition to check.
        """
        self._text_generator.append_line(f"if({if_condition})")
        # If blocks will generally end with an empty line since an empty line
        #   is added after each method call. Add an empty line at the start of
        #   the if block to make the generated CMake file more readable.
        self._text_generator.append_line()
        self.increase_indentation_level()


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
        # Create the path to the output file if it doesn't exist
        output_dir = Path(output_path).parent
        if not output_dir.exists():
            output_dir.mkdir(parents=True)

        with open(output_path, "w") as f:
            f.write(self.generate())
