import os
from pathlib import Path
from pymake.tracing.caller_info_formatter import ICallerInfoFormatter
from pymake.tracing.caller_info import CallerInfo
from pymake.tracing.traced import ITraced, Traced
from typing import Any

class ShortenedCallerInfoFormatter(ICallerInfoFormatter):
    """
    Formatter that conditionally shortens printed file paths.
    Printed file paths will be shortened into a relative path if the path is
      descended from the path passed to the constructor.
    """
    def __init__(self, base_path: Path | str):
        """
        Initializes the formatter.
        @param base_path Path to use when shortening caller info data. Must be
          an absolute path. If the caller's file path is descended from this
          path, the file path will be shortened into a path relative to this
          path.
        @throws ValueError Thrown if `base_path` is not an absolute path.
        """
        if isinstance(base_path, str):
            base_path = Path(base_path)

        if not base_path.is_absolute():
            raise ValueError("base_path must be an absolute path.")

        self._base_path = base_path.resolve()

    def format(self, x: CallerInfo | ITraced | Traced[Any]) -> str:
        """
        Converts the caller info data into a formatted string.
        @param x Object providing caller info data.
        """
        if isinstance(x, CallerInfo):
            caller_info = x
        elif isinstance(x, ITraced):
            caller_info = x.origin
        else:
            caller_info = x.call_site

        # Check if the caller's file path should be shortened
        file_path = os.path.commonprefix([
            caller_info.file_path,
            self._base_path
        ])
        return f"{file_path}:{caller_info.line_number}"

