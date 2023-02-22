from collections.abc import Iterator
from pymake.tracing.traced import Traced
from typing import Dict, Generic, TypeVar

T = TypeVar("T")

class TracedSet(Generic[T]):
    """
    A set that automatically captures tracing information for added values.
    """
    def __init__(self):
        """
        Initializes the set.
        """
        self._values: Dict[T, Traced[T]] = {}


    def __bool__(self) -> bool:
        """
        Checks whether the set is not empty.
        """
        return bool(self._values)


    def __contains__(self, value: T) -> bool:
        """
        Checks whether the set contains the value.
        """
        return value in self._values


    def __iter__(self) -> Iterator[Traced[T]]:
        """
        Allows each traced value in the set to be iterated over.
        """
        return (v for v in self._values.values())


    def add(self, value: T) -> None:
        """
        Adds a new value to the set.
        @param value Value to add to the set.
        @throws ValueError Thrown if the set already contains the value.
        """
        if value in self._values:
            call_site = self._values[value].origin
            raise ValueError(
                "Value already exists in the set: '{value}'.\n" +
                "Note - value was previously added at " +
                f"'{call_site.file_path}':'{call_site.line_number}'"
            )
        self._values[value] = Traced(value)
