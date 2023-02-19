from typing import Iterable, Optional

class CodeGenerator:
    """
    Helper type used to format a code string to make it easy for humans to read.
    """
    def __init__(self, use_spaces: bool = False, tab_size: int = 4):
        """
        Initializes the generator.
        @param use_spaces Whether spaces should be used in the generated files.
        @param tab_size Only used if `use_spaces` is true. Determines the number
          of spaces inserted for each indentation level.
        """
        # String that will be added to as code is generated
        self._code = ""

        # Current indentation level to use for newly added text.
        self._indent_level = 0

        if use_spaces:
            self._indent = " " * tab_size
        else:
            self._indent = "\t"

    @property
    def code(self) -> str:
        """
        Gets the string containing the generated code.
        """
        return self._code

    def append(self, text: str) -> None:
        """
        Adds text to the generator.
        This method will not append a newline character to the added text.
        @param text Text to add.
        """
        # If the generator is at the start of a new line, apply the indentation
        #   level before adding the text
        if len(self._code) > 0 and self._code[-1] == "\n":
            self.apply_indentation()

        self._code += text

    def append_line(self, text: str) -> None:
        """
        Adds text to the generator.
        This method will append a newline character to the added text.
        @param text Text to add.
        """
        self.append(text + "\n")

    def apply_indentation(self) -> None:
        """
        Adds whitespace characters to apply the current indentation level.
        """
        self._code += self._indent * self._indent_level

    def close_method(self) -> None:
        """
        Closes the currently open method block.
        @pre A method block is currently open.
        """
        self.decrease_indentation_level()
        self.append_line(")")

    def decrease_indentation_level(self, delta: int = 1) -> None:
        """
        Decreases the indentation level by the specified amount.
        @param delta Amount to decrease the indentation level by. Must be a
          value greater than or equal to 0.
        """
        assert delta >= 0
        self.modify_indentation_level(-delta)

    def increase_indentation_level(self, delta: int = 1) -> None:
        """
        Increases the indentation level by the specified amount.
        @param delta Amount to increase the indentation level by. Must be a
          value greater than or equal to 0.
        """
        assert delta >= 0
        self.modify_indentation_level(delta)

    def modify_indentation_level(self, delta: int) -> None:
        """
        Modifies the current indentation level by the specified amount.
        @param delta Amount to increase or decrease the indentation level by.
        """
        self._indent_level += delta
        self._indent_level = max(self._indent_level, 0)

    def open_method(self, method_name: str) -> None:
        """
        Opens a new method block.
        @param method_name Name of the method to open.
        """
        self.append_line(method_name + "(")
        self.increase_indentation_level()

    def write_method_parameter(self,
        keyword: Optional[str],
        values: str | Iterable[str]) -> None:
        """
        Writes a CMake method parameter to the generator.
        @param keyword CMake keyword to write before the arguments. If not
          provided, nothing will be written before the arguments.
        @param values Values to pass in via the method parameter.
        """
        # Make the `values` parameter into an iterable if it isn't already one
        if isinstance(values, str):
            values = [values]

        # If a keyword is present, push values up by one indentation level to
        #   improve readability
        if keyword:
            self.append_line(keyword)
            self.increase_indentation_level()

        for v in values:
            self.append_line(v)

        if keyword:
            self.decrease_indentation_level()
