from pathlib import Path
from pymake.tracing.caller_info import CallerInfo
from typing import Dict, Generic, TypeVar

T = TypeVar("T")

class ITraced:
    """
    Interface implemented by classes that provide tracing data for themselves.
    """
    def __init__(self,
        origin: CallerInfo | None = None):
        """
        Initializes the object.
        @param origin Call site where the object was constructed. If not
          provided, the call site will be determined automatically by capturing
          the first external frame.
        """
        self._origin = origin if origin else CallerInfo.closest_external_frame()


    @property
    def origin(self) -> CallerInfo:
        """
        Gets the location that constructed the object.
        """
        return self._origin


    @property
    def file_path(self) -> Path:
        """
        Gets the file path where the object was constructed.
        """
        return self._origin.file_path


    @property
    def file_dir(self) -> Path:
        """
        Gets the directory where the object was constructed.
        """
        return self._origin.file_path.parent


    @property
    def line_number(self) -> int:
        """
        Gets the line number where the object was constructed.
        """
        return self._origin.line_number


class Traced(Generic[T], ITraced):
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
        super().__init__(call_site)
        self._value = value


    def to_dict(self) -> Dict[str, object]:
        """
        Converts the object to a dictionary that can be written to a trace file.
        """
        return {
            "value": str(self._value),
            "origin": {
                "file": str(self.origin.file_path),
                "line": self.origin.line_number
            }
        }


    @property
    def value(self) -> T:
        """
        Retrieves the wrapped value.
        """
        return self._value
