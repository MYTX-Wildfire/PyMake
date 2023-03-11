from pymake.tracing.caller_info import CallerInfo
from pymake.tracing.traced import ITraced
from typing import Dict, Generic, Iterator, Tuple, TypeVar

Key = TypeVar("Key")
Value = TypeVar("Value", bound=ITraced)

class TracedDict(Generic[Key, Value]):
    """
    A dictionary that allows lookup by key or origin.
    """
    def __init__(self):
        """
        Initializes the dictionary.
        """
        ## Dictionary used to look up values by key
        # @invariant len(self._values_by_name) == len(self._values_by_origin)
        self._values_by_name: Dict[Key, Value] = {}

        ## Dictionary used to look up values by origin
        # @invariant len(self._values_by_name) == len(self._values_by_origin)
        self._values_by_origin: Dict[CallerInfo, Value] = {}


    def __bool__(self) -> bool:
        """
        Checks whether the dictionary is not empty.
        """
        return bool(self._values_by_name)


    def __contains__(self, key: Key | CallerInfo) -> bool:
        """
        Checks whether the dictionary contains the key.
        @param key Key to check for or origin to check for.
        """
        if isinstance(key, CallerInfo):
            return key in self._values_by_origin
        return key in self._values_by_name


    def __getitem__(self, key: Key | CallerInfo) -> Value:
        """
        Gets the value from the dictionary.
        @param key Key to get the value for or origin to get the value for.
        """
        if isinstance(key, CallerInfo):
            return self._values_by_origin[key]
        return self._values_by_name[key]


    def __iter__(self) -> Iterator[Tuple[Key, Value]]:
        """
        Allows each value in the dictionary to be iterated over.
        """
        return ((k, v) for k, v in self._values_by_name.items())


    def __len__(self) -> int:
        """
        Gets the number of values in the dictionary.
        """
        return len(self._values_by_name)


    def __setitem__(self, key: Key, value: Value) -> None:
        """
        Sets the value for the given key, overwriting any previous value.
        @param key Key to set the value for.
        @param value Value to set for the given key.
        """
        self._values_by_name[key] = value
        self._values_by_origin[value.origin] = value


    def add(self, key: Key, value: Value) -> bool:
        """
        Adds a new value to the dictionary if it doesn't exist.
        @param key Key to add the value under.
        @param value Value to add to the dictionary. This must be a traced value
          or a traced object. If the object is a traced object, `Value` must be
          a subclass of `ITraced`.
        @returns True if the value was added, False if the key already exists.
        """
        if key in self._values_by_name:
            return False

        self._values_by_name[key] = value
        self._values_by_origin[value.origin] = value
        return True


    def keys(self) -> Iterator[Key]:
        """
        Gets the keys in the dictionary.
        """
        for key in self._values_by_name.keys():
            yield key


    def values(self) -> Iterator[Value]:
        """
        Gets the values in the dictionary.
        """
        for value in self._values_by_name.values():
            yield value


    def origins(self) -> Iterator[CallerInfo]:
        """
        Gets the origins in the dictionary.
        """
        for origin in self._values_by_origin.keys():
            yield origin
