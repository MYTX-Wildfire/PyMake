from pymake.tracing.caller_info import CallerInfo
from pymake.tracing.caller_info_formatter import ICallerInfoFormatter
from pymake.tracing.traced import ITraced, Traced
from typing import Any

class MockCallerInfoFormatter(ICallerInfoFormatter):
    """
    Caller info formatter used for testing.
    """
    def __init__(self, output: str):
        """
        Initializes the formatter.
        @param output Output to return from the `format` method.
        """
        self._output = output


    def format(self, x: CallerInfo | ITraced | Traced[Any]) -> str:
        """
        Converts the caller info data into a formatted string.
        @param x Object providing caller info data.
        """
        return self._output
