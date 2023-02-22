from pymake.tracing.caller_info_formatter import ICallerInfoFormatter
from pymake.tracing.caller_info import CallerInfo
from pymake.tracing.traced import ITraced, Traced
from typing import Any

class NullCallerInfoFormatter(ICallerInfoFormatter):
    """
    Formatter that always returns empty strings.
    """

    def format(self, x: CallerInfo | ITraced | Traced[Any]) -> str:
        """
        Converts the caller info data into a formatted string.
        @param x Object providing caller info data.
        """
        return ""
