from __future__ import annotations
from collections.abc import Iterator
from pymake.tracing.caller_info import CallerInfo
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
        self._values = values if values else {}


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


    def __getitem__(self, value: T) -> Traced[T]:
        """
        Gets the traced value from the set.
        @param value Value to get the traced value for.
        @returns The traced value for the given value.
        """
        return self._values[value]


    def __iter__(self) -> Iterator[Traced[T]]:
        """
        Allows each traced value in the set to be iterated over.
        """
        return (v for v in self._values.values())


    def __len__(self) -> int:
        """
        Gets the number of values in the set.
        """
        return len(self._values)


    def add(self, value: T, origin: Optional[CallerInfo] = None) -> bool:
        """
        Adds a new value to the set.
        @param value Value to add to the set.
        @param origin The origin of the value. If this is set to `None`, the
          origin will be automatically captured.
        @returns True if the value was added, False if it was already in the set.
        """
        if value in self._values:
            return False
        if origin is None:
            origin = CallerInfo.closest_external_frame()

        self._values[value] = Traced(value, origin)
        return True


    def clone(self) -> TracedSet[T]:
        """
        Creates a clone of the set.
        @returns A clone of the set.
        """
        return TracedSet(self._values.copy())


    def merge(self, other: TracedSet[T]) -> None:
        """
        Merges the values from another set into this set.
        @param other Set to merge values from.
        """
        for value in other:
            self._values[value.value] = value
