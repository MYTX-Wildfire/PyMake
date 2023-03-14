class TextGenerator:
    """
    Helper type used to format a text string to make it easy for humans to read.
    """
    def __init__(self, use_spaces: bool = False, tab_size: int = 4):
        """
        Initializes the generator.
        @param use_spaces Whether spaces should be used in the generated string.
        @param tab_size Only used if `use_spaces` is true. Determines the number
          of spaces inserted for each indentation level.
        """
        # String that will be added to as text is generated
        self._text = ""

        # Current indentation level to use for newly added text.
        self._indent_level = 0

        if use_spaces:
            self._indent = " " * tab_size
        else:
            self._indent = "\t"


    @property
    def at_start_of_line(self) -> bool:
        """
        Gets whether the generator is at the start of a new line.
        """
        return len(self._text) == 0 or self._text[-1] == "\n"


    @property
    def indentation_level(self) -> int:
        """
        Gets the current indentation level.
        """
        return self._indent_level


    @indentation_level.setter
    def indentation_level(self, value: int) -> None:
        """
        Sets the current indentation level.
        @param value New indentation level.
        @throws ValueError Thrown if the indentation level is negative.
        """
        if value < 0:
            raise ValueError(
                "Indentation level must be greater than or equal to 0."
            )

        self._indent_level = value


    @property
    def text(self) -> str:
        """
        Gets the string containing the generated text.
        """
        return self._text


    def append(self, text: str) -> None:
        """
        Adds text to the generator.
        This method will not append a newline character to the added text.
        @param text Text to add.
        """
        # If the generator is at the start of a new line, apply the indentation
        #   level before adding the text
        if len(self._text) > 0 and self._text[-1] == "\n":
            self.apply_indentation()

        self._text += text


    def append_line(self, text: str = "") -> None:
        """
        Adds text to the generator.
        This method will append a newline character to the added text.
        @param text Text to add.
        """
        if self.at_start_of_line:
            self.apply_indentation()
        self.append(text + "\n")


    def apply_indentation(self) -> None:
        """
        Adds whitespace characters to apply the current indentation level.
        """
        self._text += self._indent * self._indent_level


    def decrease_indentation_level(self, delta: int = 1) -> None:
        """
        Decreases the indentation level by the specified amount.
        @param delta Amount to decrease the indentation level by. Must be a
          value greater than or equal to 0.
        """
        assert delta >= 0
        self.modify_indentation_level(-delta)


    def finish_line(self) -> None:
        """
        Finishes the current line if not currently on a new line.
        """
        if not self.at_start_of_line:
            self.append_line("")


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
          If this is negative and the resulting indentation level is less than
          zero, the indentation level will be clamped to zero.
        """
        self._indent_level += delta
        self._indent_level = max(self._indent_level, 0)


    def remove_last_instance_of(self, text: str) -> bool:
        """
        Removes the last instance of the specified text from the generator.
        @param text Text to remove.
        @returns True if the text was found and removed; otherwise, false.
        """
        index = self._text.rfind(text)
        if index >= 0:
            self._text = self._text[:index] + self._text[index + len(text):]
        return index >= 0
