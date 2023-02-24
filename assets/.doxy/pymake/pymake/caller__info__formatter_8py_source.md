
# File caller\_info\_formatter.py

[**File List**](files.md) **>** [**pymake**](dir_07157586182338563a5b56382e54f8e9.md) **>** [**tracing**](dir_75df20bd24a370a7d657bc0a1251e8dc.md) **>** [**caller\_info\_formatter.py**](caller__info__formatter_8py.md)

[Go to the documentation of this file.](caller__info__formatter_8py.md) 

```Python

from abc import ABC, abstractmethod
from pymake.tracing.caller_info import CallerInfo
from pymake.tracing.traced import ITraced, Traced
from typing import Any

class ICallerInfoFormatter(ABC):
    """
    Base class for types that format data from a `CallerInfo` instance.
    """
    @abstractmethod
    def format(self, x: CallerInfo | ITraced | Traced[Any]) -> str:
        """
        Converts the caller info data into a formatted string.
        @param x Object providing caller info data.
        """
        raise NotImplementedError()

```