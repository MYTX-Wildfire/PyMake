import inspect
from pathlib import Path

class CallerInfo:
    """
    Helper class that captures caller information for a method.
    """
    def __init__(self, caller_stack_offset: int = 2):
        """
        Initializes the object.
        @param caller_stack_offset Number of stack frames to traverse to get to
          the stack frame of the caller whose data should be captured. This is
          measured from the `CallerInfo`'s stack frame, so this value must be
          at least 1. However, since a value of 1 will retrieve the information
          of the method constructing the `CallerInfo` object, the default value
          for this parameter is set to 2 so that the caller of the method
          constructing this object is retrieved.
        """
        assert caller_stack_offset > 0

        # Get the frame for the caller whose information should be captured
        frame = inspect.currentframe()
        for _ in range(caller_stack_offset):
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
