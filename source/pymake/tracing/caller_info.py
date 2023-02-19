from __future__ import annotations
import inspect
import os
from pathlib import Path

class CallerInfo:
    """
    Helper class that captures caller information for a method.
    """
    def __init__(self, caller_stack_offset: int):
        """
        Initializes the object.
        @param caller_stack_offset Number of stack frames to traverse to get to
          the stack frame of the caller whose data should be captured.
        """
        assert caller_stack_offset >= 0

        # Get the frame for the caller whose information should be captured
        # Note that 1 is added to the offset passed to this method to account
        #   for this class's constructor's stack frame.
        frame = inspect.currentframe()
        for _ in range(caller_stack_offset + 1):
            assert frame
            frame = frame.f_back

        # Make sure that a stack frame exists at the target level
        assert frame

        # Capture the information so that it can be used later
        # Note that `frame` must not be stored and used to get the values later.
        #   Attempting to do so will return values correct at the point that
        #   the frame's values are accessed, not the time when the frame was
        #   constructed.
        self._file_path = Path(frame.f_code.co_filename).absolute().resolve()
        self._line_number = frame.f_lineno

    @staticmethod
    def closest_external_frame() -> CallerInfo:
        """
        Creates a `CallerInfo` instance for the closest non-pymake stack frame.
        """
        i = 1
        caller_info = CallerInfo(i)
        sep = os.path.sep
        while f"{sep}pymake{sep}" in str(caller_info.file_path):
            i += 1
            caller_info = CallerInfo(i)
        return caller_info

    @property
    def file_path(self) -> Path:
        """
        Gets the file path of the caller's code.
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
