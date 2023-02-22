from pymake.tracing.traced import Traced
from typing import Any

class YamlGenerator:
    """
    Helper type used to write values out in YAML format.
    """
    def __init__(self, tab_size: int = 2):
        """
        Initializes the generator.
        @param tab_size Determines the number of spaces inserted for each
          indentation level.
        """
        # String that will be added to as text is generated
        self._text = "---\n"

        # Current indentation level to use for newly added text.
        self._indent_level = 0

        # String to insert to apply an indentation level
        self._indent = " " * tab_size

    @property
    def text(self) -> str:
        """
        Gets the string containing the generated text.
        """
        if self._text and self._text[-1] != "\n":
            suffix = "\n"
        else:
            suffix = ""
        suffix += "...\n"

        return self._text + suffix

    def append(self, text: str) -> None:
        """
        Adds text to the generator.
        This method will not append a newline character to the added text.
        @param text Text to add.
        """
        # If the generator is at the start of a new line, apply the indentation
        #   level before adding the text
        if self._text and self._text[-1] == "\n":
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

    def write_block_pair(self,
        key: str,
        value: str,
        add_quotes: bool = True) -> None:
        """
        Writes a key-value pair to the current block.
        @param key Key that the value is associated with.
        @param value Value to write.
        @param add_quotes Whether to add quotation marks around the value when
          writing it.
        """
        if add_quotes:
            self.append_line(f"{key}: \"{value}\"")
        else:
            self.append_line(f"{key}: {value}")

    def write_block_value(self, value: str, add_quotes: bool = True) -> None:
        """
        Writes a value to the current block.
        @param value Value to write.
        @param add_quotes Whether to add quotation marks around the value when
          writing it.
        """
        if add_quotes:
            self.append_line(f"- \"{value}\"")
        else:
            self.append_line(f"- {value}")

    def write_empty_dict(self, key: str) -> None:
        """
        Writes an empty dictionary to the current block.
        @param key Key to use for the dictionary.
        """
        self.append_line(f"{key}: {{}}")

    def write_traced(self,
        key: str,
        value: Traced[Any],
        add_quotes: bool = True) -> None:
        """
        Writes a traced value as a YAML dictionary.
        @param key Key to use as the name of the dictionary.
        @param value Traced value containing the value to write and the tracing
          information to add.
        @param add_quotes Whether to add quotation marks around the values being
          written out.
        """
        self.open_block(key)
        self.write_block_pair("value", value.value, add_quotes)
        self.write_block_pair(
            "origin",
            f"{value.origin.file_path}:{value.origin.line_number}",
        )
        self.close_block()
