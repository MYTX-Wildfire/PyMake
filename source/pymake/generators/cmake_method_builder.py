from __future__ import annotations
from pymake.generators.text_generator import TextGenerator
from pymake.tracing.caller_info import CallerInfo
from pymake.tracing.caller_info_formatter import ICallerInfoFormatter
from types import TracebackType
from typing import Optional, Type

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
        caller_info = CallerInfo.closest_external_frame()
        caller_info_str = formatter.format(caller_info)
        self._generator = generator
        self._arguments_added = False

        # Only add the tracing information if it's not empty
        if caller_info_str:
            self._generator.append_line(f"# {formatter.format(caller_info)}")

        # Open the method
        self._generator.append_line(f"{method_name}(")
        self._generator.indentation_level += 1


    def add_arguments(self, *args: str) -> None:
        """
        Adds keyword-less argument(s) to the method.
        @param args Argument(s) to add. If this is empty, this method will be
          a no-op.
        """
        if not args:
            return

        self._arguments_added = True
        for arg in args:
            self._generator.append_line(arg)


    def add_keyword_arguments(self,
        keyword: str,
        *args: str) -> None:
        """
        Adds argument(s) under a method parameter keyword to the method.
        @param keyword Keyword to use.
        @param args Argument(s) to add. Must not be empty.
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
            self._generator.append_line(arg)
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
