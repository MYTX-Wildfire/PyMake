from pymake.tracing.caller_info_formatter import ICallerInfoFormatter
from pymake.tracing.caller_info import CallerInfo
from pymake.tracing.traced import ITraced, Traced
from typing import Any

class FullCallerInfoFormatter(ICallerInfoFormatter):
    """
    Formatter that always prints full paths.
    """

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

        return f"{caller_info.file_path}:{caller_info.line_number}"
