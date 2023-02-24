
# File null\_caller\_info\_formatter.py

[**File List**](files.md) **>** [**pymake**](dir_07157586182338563a5b56382e54f8e9.md) **>** [**tracing**](dir_75df20bd24a370a7d657bc0a1251e8dc.md) **>** [**null\_caller\_info\_formatter.py**](null__caller__info__formatter_8py.md)

[Go to the documentation of this file.](null__caller__info__formatter_8py.md) 

```Python

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

```