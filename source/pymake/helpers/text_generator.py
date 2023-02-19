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
        self._text += self._indent * self._indent_level

    def close_block(self) -> None:
        """
        Closes the currently open block.
        @pre A method block is currently open.
        """
        self.decrease_indentation_level()

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

    def open_block(self, block_name: str) -> None:
        """
        Opens a new block.
        @param block_name Name of the block to open.
        """
        self.append_line(block_name + ":")
        self.increase_indentation_level()

    def write_block_pair(self, key: str, value: str) -> None:
        """
        Writes a key-value pair to the current block.
        @param key Key that the value is associated with.
        @param value Value to write.
        """
        self.append_line(f"{key}: {value}")

    def write_block_value(self, value: str) -> None:
        """
        Writes a value to the current block.
        @param value Value to write.
        """
        self.append_line(f"- {value}")

