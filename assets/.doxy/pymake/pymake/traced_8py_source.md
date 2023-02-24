
# File traced.py

[**File List**](files.md) **>** [**pymake**](dir_07157586182338563a5b56382e54f8e9.md) **>** [**tracing**](dir_75df20bd24a370a7d657bc0a1251e8dc.md) **>** [**traced.py**](traced_8py.md)

[Go to the documentation of this file.](traced_8py.md) 

```Python

from pymake.tracing.caller_info import CallerInfo
from typing import Dict, Generic, TypeVar

T = TypeVar("T")

class ITraced:
    """
    Interface implemented by classes that provide tracing data for themselves.
    """
    def __init__(self):
        """
        Initializes the object.
        """
        self._origin_origin = CallerInfo.closest_external_frame()


    @property
    def origin(self) -> CallerInfo:
        """
        Gets the location that constructed the object.
        """
        return self._origin_origin


class Traced(Generic[T]):
    """
    Wrapper used to add tracing information to a value.
    """
    def __init__(self, value: T, call_site: CallerInfo | None = None):
        """
        Initializes the object.
        @param value Value to wrap.
        @param call_site Call site where the value was provided from. If not
          provided, the call site will be determined automatically by capturing
          the first external frame.
        """
        self._value_value = value
        self._origin_origin = (call_site if call_site
            else CallerInfo.closest_external_frame())


    def to_dict(self) -> Dict[str, object]:
        """
        Converts the object to a dictionary that can be written to a trace file.
        """
        return {
            "value": str(self._value_value),
            "origin": {
                "file": str(self._origin_origin.file_path),
                "line": self._origin_origin.line_number
            }
        }


    @property
    def origin(self) -> CallerInfo:
        """
        Returns the call site where the value was provided from.
        """
        return self._origin_origin


    @property
    def value(self) -> T:
        """
        Retrieves the wrapped value.
        """
        return self._value_value

```