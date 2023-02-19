from pymake.tracing.caller_info import CallerInfo
from typing import Generic, TypeVar

T = TypeVar('T')

class Traced(Generic[T]):
    """
    Wrapper used to add tracing information to a value.
    """
    def __init__(self, value: T):
        """
        Initializes the object.
        @param value Value to wrap.
        """
        self._value = value
        self._call_site = CallerInfo.closest_external_frame()

    @property
    def call_site(self) -> CallerInfo:
        """
        Returns the call site where the value was provided from.
        """
        return self._call_site

    @property
    def value(self) -> T:
        """
        Retrieves the wrapped value.
        """
        return self._value
