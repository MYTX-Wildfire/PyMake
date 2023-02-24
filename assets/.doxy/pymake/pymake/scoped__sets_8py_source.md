
# File scoped\_sets.py

[**File List**](files.md) **>** [**core**](dir_b275da0bd59d7f0b7cbb72771801f871.md) **>** [**scoped\_sets.py**](scoped__sets_8py.md)

[Go to the documentation of this file.](scoped__sets_8py.md) 

```Python

from __future__ import annotations
from pymake.common.scope import EScope
from pymake.tracing.traced_set import TracedSet
from typing import Dict, Generic, Optional, TypeVar

T = TypeVar("T")

class ScopedSets(Generic[T]):
    """
    Collection of sets with different scopes.
    An instance of this class is used for most target properties that support
      multiple scope levels.
    """

    def __init__(self,
        public: Optional[TracedSet[T]] = None,
        interface: Optional[TracedSet[T]] = None,
        private: Optional[TracedSet[T]] = None):
        """
        Initializes the set.
        @param public Public values to add to the set.
        @param interface Interface values to add to the set.
        @param private Private values to add to the set.
        """
        self._public: TracedSet[T] = public if public else TracedSet()
        self._interface: TracedSet[T] = interface if interface else TracedSet()
        self._private: TracedSet[T] = private if private else TracedSet()


    @property
    def public(self) -> TracedSet[T]:
        """
        Gets the public values in the set.
        """
        return self._public


    @property
    def interface(self) -> TracedSet[T]:
        """
        Gets the interface values in the set.
        """
        return self._interface


    @property
    def private(self) -> TracedSet[T]:
        """
        Gets the private values in the set.
        """
        return self._private


    def to_trace_dict(self) -> Dict[str, object]:
        """
        Converts the set to a dictionary that can be written to a trace file.
        """
        return {
            "public": [t.to_dict() for t in self._public],
            "interface": [t.to_dict() for t in self._interface],
            "private": [t.to_dict() for t in self._private]
        }


    def select_set(self, scope: EScope) -> TracedSet[T]:
        """
        Gets the set for the specified scope.
        @param scope Scope to get the set for.
        @throws ValueError If the specified scope is invalid.
        @returns Set for the specified scope.
        """
        if scope == EScope.PUBLIC:
            return self._public
        if scope == EScope.INTERFACE:
            return self._interface
        if scope == EScope.PRIVATE:
            return self._private
        raise ValueError(f"Invalid scope: '{scope}'")


    def __bool__(self) -> bool:
        """
        Checks whether the set contains any values.
        @returns True if the set contains any values.
        """
        return bool(self._public) or bool(self._interface) or bool(self._private)

```