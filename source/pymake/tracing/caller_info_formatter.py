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
