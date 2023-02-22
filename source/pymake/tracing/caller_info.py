from __future__ import annotations
import inspect
import os
from pathlib import Path

class CallerInfo:
    """
    Helper class that captures caller information for a method.
    """
    def __init__(self, file_path: Path, line_number: int):
        """
        Initializes the object.
        @param file_path Absolute path to the file that the stack frame is from.
        @param line_number Line number of the executing code whose stack frame
          is captured.
        """
        self._file_path = file_path
        self._line_number = line_number

    @staticmethod
    def closest_external_frame() -> CallerInfo:
        """
        Creates a `CallerInfo` instance for the closest non-pymake stack frame.
        @returns A `CallerInfo` instance that captures the data for the closest
          non-pymake stack frame.
        """
        i = 1
        caller_info = CallerInfo.from_stack_frame(i)
        sep = os.path.sep
        while f"{sep}pymake{sep}" in str(caller_info.file_path):
            i += 1
            caller_info = CallerInfo.from_stack_frame(i)
        return caller_info

    @staticmethod
    def from_stack_frame(offset: int) -> CallerInfo:
        """
        Generates a caller info instance from the target stack frame.
        @param offset Offset in numbers of stack frames from the caller method
          to capture in the `CallerInfo` instance. A value of 0 will capture
          the caller method's stack frame.
        """
        # Get the frame for the caller whose information should be captured
        # Note that 1 is added to the offset passed to this method to account
        #   for this method's stack frame.
        frame = inspect.currentframe()
        for _ in range(0, offset + 1):
            assert frame
            frame = frame.f_back

        # Make sure that a stack frame exists at the target level
        assert frame

        # Capture the information so that it can be used later
        # Note that `frame` must not be stored and used to get the values later.
        #   Attempting to do so will return values correct at the point that
        #   the frame's values are accessed, not the time when the frame was
        #   constructed.
        file_path = Path(frame.f_code.co_filename).absolute().resolve()
        line_number = frame.f_lineno
        return CallerInfo(file_path, line_number)

    @property
    def file_path(self) -> Path:
        """
        Gets the file path of the caller's code.
        @invariant This will always be an absolute path.
        """
        return self._file_path

    @property
    def line_number(self) -> int:
        """
        Gets the line number of the caller's code.
        """
        return self._line_number

    def __hash__(self) -> int:
        """
        Generates the hash of the object.
        @returns The hash of the object.
        """
        return hash((self._file_path, self._line_number))

    def __eq__(self, other: object) -> bool:
        """
        Checks if the other object is equal to this object.
        @param other Object to compare to this object.
        @returns True if the two objects are equal.
        """
        if isinstance(other, CallerInfo):
            return (
                self._file_path,
                self._line_number
            ) == (
                other.file_path,
                other.line_number
            )
        return False
