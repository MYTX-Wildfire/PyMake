
# File traced\_set.py

[**File List**](files.md) **>** [**pymake**](dir_07157586182338563a5b56382e54f8e9.md) **>** [**tracing**](dir_75df20bd24a370a7d657bc0a1251e8dc.md) **>** [**traced\_set.py**](traced__set_8py.md)

[Go to the documentation of this file.](traced__set_8py.md) 

```Python

from __future__ import annotations
from collections.abc import Iterator
from pymake.tracing.traced import Traced
from typing import Dict, Generic, Optional, TypeVar

T = TypeVar("T")

class TracedSet(Generic[T]):
    """
    A set that automatically captures tracing information for added values.
    """
    def __init__(self,
        values: Optional[Dict[T, Traced[T]]] = None):
        """
        Initializes the set.
        @param values Dictionary of values to add to the set.
        """
        self._values_values = values if values else {}


    def __bool__(self) -> bool:
        """
        Checks whether the set is not empty.
        """
        return bool(self._values_values)


    def __contains__(self, value: T) -> bool:
        """
        Checks whether the set contains the value.
        """
        return value in self._values_values


    def __iter__(self) -> Iterator[Traced[T]]:
        """
        Allows each traced value in the set to be iterated over.
        """
        return (v for v in self._values_values.values())


    def add(self, value: T) -> None:
        """
        Adds a new value to the set.
        @param value Value to add to the set.
        @throws ValueError Thrown if the set already contains the value.
        """
        if value in self._values_values:
            call_site = self._values_values[value].origin
            raise ValueError(
                "Value already exists in the set: '{value}'.\n" +
                "Note - value was previously added at " +
                f"'{call_site.file_path}':'{call_site.line_number}'"
            )
        self._values_values[value] = Traced(value)


    def clone(self) -> TracedSet[T]:
        """
        Creates a clone of the set.
        @returns A clone of the set.
        """
        return TracedSet(self._values_values.copy())

```