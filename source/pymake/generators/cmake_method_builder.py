from __future__ import annotations
from pymake.generators.text_generator import TextGenerator
from pymake.tracing.caller_info_formatter import ICallerInfoFormatter
from pymake.tracing.traced import Traced
from types import TracebackType
from typing import Any, Optional, Type

class CMakeMethodBuilder:
    """
    Helper type used to generate a CMake method.
    """
    def __init__(self,
        formatter: ICallerInfoFormatter,
        generator: TextGenerator,
        method_name: str):
        """
        Initializes the builder.
        @param generator Generator to write the generated code to.
        @param method_name Name of the method.
        """
        self._formatter = formatter
        self._generator = generator
        self._arguments_added = False

        # Open the method
        self._generator.append_line(f"{method_name}(")
        self._generator.indentation_level += 1


    def add_arguments(self,
        *args: Any | Traced[Any],
        add_quotes: bool = False) -> None:
        """
        Adds keyword-less argument(s) to the method.
        @param args Argument(s) to add. If this is empty, this method will be
          a no-op.
        @param add_quotes Whether to add quotes around the argument.
        """
        if not args:
            return
        self._arguments_added = True

        for arg in args:
            self._write_arg(arg, add_quotes)


    def add_keyword_arguments(self,
        keyword: str,
        *args: Any | Traced[Any],
        add_quotes: bool = False) -> None:
        """
        Adds argument(s) under a method parameter keyword to the method.
        @param keyword Keyword to use.
        @param args Argument(s) to add. Must not be empty.
        @param add_quotes Whether to add quotes around the argument.
        @throws RuntimeError Thrown if `args` is empty.
        """
        if not args:
            raise RuntimeError("No arguments provided.")
        self._arguments_added = True

        # Place the keyword on the current indentation level, then use an
        #   increased indentation level for the arguments
        self._generator.append_line(f"{keyword}")
        self._generator.increase_indentation_level()
        for arg in args:
            self._write_arg(arg, add_quotes)
        self._generator.decrease_indentation_level()


    def __enter__(self) -> CMakeMethodBuilder:
        """
        Enters the method block.
        """
        return self


    def __exit__(self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType]) -> None:
        """
        Exits the method block.
        @param exc_type Type of exception that was raised.
        @param exc_value Value of the exception that was raised.
        @param traceback Traceback of the exception that was raised.
        @returns True if the exception should be suppressed, otherwise False.
        """
        # If no arguments were added, remove the newline character that was
        #   added after the opening parenthesis
        if not self._arguments_added:
            self._generator.remove_last_instance_of("\n")
        else:
            # This should be a no-op, but is included just in case
            self._generator.finish_line()

        # Finish the line with the parenthesis and add a new line afterwards
        #   to separate this method call from the next line of code
        self._generator.decrease_indentation_level()
        self._generator.append_line(")\n")


    def _write_arg(self,
        arg: Any | Traced[Any],
        add_quotes: bool) -> None:
        """
        Writes an argument to the generator.
        @param arg Argument to write.
        @param add_quotes Whether to add quotes around the argument.
        """
        if isinstance(arg, Traced):
            self._write_traced(arg, add_quotes)
        else:
            self._write_line(arg, add_quotes)


    def _write_traced(self,
        traced: Traced[Any],
        add_quotes: bool) -> None:
        """
        Adds a traced value to the method.
        @param traced Traced value to add.
        @param add_quotes Whether to add quotes around the argument.
        """
        self._generator.append_line(
            f"# {self._formatter.format(traced)}"
        )
        self._write_line(traced.value, add_quotes)


    def _write_line(self,
        value: Any,
        add_quotes: bool) -> None:
        """
        Writes a value to the generator.
        @param value Value to write.
        @param add_quotes Whether to add quotes around the argument.
        """
        if add_quotes:
            self._generator.append_line(f"\"{value}\"")
        else:
            self._generator.append_line(f"{value}")
