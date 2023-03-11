from pathlib import Path
from typing import Optional

class CMakeConfigTargetProperties:
    """
    Stores config-specific CMake target properties.
    """
    def __init__(self):
        """
        Initializes the CMake config-specific target properties with default values.
        """
        ## The name of the imported library for the current configuration.
        self._imported_library_name: Optional[str] = None

        ## The name of the implementation library for the current configuration.
        self._imported_implib_name: Optional[str] = None

        ## The path of the imported location for the current configuration.
        # @invariant This will always be an absolute path.
        self._imported_location: Optional[Path] = None
