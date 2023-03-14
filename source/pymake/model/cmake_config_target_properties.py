from pathlib import Path
from pymake.tracing.traced import ITraced, Traced
from typing import Optional

class CMakeConfigTargetProperties(ITraced):
    """
    Stores config-specific CMake target properties.
    """
    def __init__(self):
        """
        Initializes the CMake config-specific target properties with default values.
        """
        super().__init__()

        ## The name of the imported library for the current configuration.
        self._imported_libname: Traced[Optional[str]] = Traced(None)

        ## The name of the implementation library for the current configuration.
        self._imported_implib_name: Traced[Optional[str]] = Traced(None)

        ## The path of the imported location for the current configuration.
        # @invariant This will always be an absolute path.
        self._imported_location: Traced[Optional[Path]] = Traced(None)


    @property
    def imported_libname(self) -> Traced[Optional[str]]:
        """
        Gets the name of the imported library for the current configuration.
        """
        return self._imported_libname


    @imported_libname.setter
    def imported_libname(self, value: Optional[str]) -> None:
        """
        Sets the name of the imported library for the current configuration.
        """
        self._imported_libname = Traced(value)


    @property
    def imported_implib_name(self) -> Traced[Optional[str]]:
        """
        Gets the name of the implementation library for the current configuration.
        """
        return self._imported_implib_name


    @imported_implib_name.setter
    def imported_implib_name(self, value: Optional[str]) -> None:
        """
        Sets the name of the implementation library for the current configuration.
        """
        self._imported_implib_name = Traced(value)


    @property
    def imported_location(self) -> Traced[Optional[Path]]:
        """
        Gets the path of the imported location for the current configuration.
        """
        return self._imported_location


    @imported_location.setter
    def imported_location(self, value: Optional[Path]) -> None:
        """
        Sets the path of the imported location for the current configuration.
        """
        self._imported_location = Traced(value)
