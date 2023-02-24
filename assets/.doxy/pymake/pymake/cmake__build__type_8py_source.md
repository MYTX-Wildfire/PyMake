
# File cmake\_build\_type.py

[**File List**](files.md) **>** [**common**](dir_3ab6d032c6cf1bbf53e47468d3941a46.md) **>** [**cmake\_build\_type.py**](cmake__build__type_8py.md)

[Go to the documentation of this file.](cmake__build__type_8py.md) 

```Python

from enum import Enum

class ECMakeBuildType(Enum):
    """
    Defines constants for each built in CMake build type.
    """
    # Debug build type.
    Debug = "Debug"

    # Release build type.
    Release = "Release"

    # Release with Debug Info build type.
    RelWithDebInfo = "RelWithDebInfo"

    # Minimum Size Release build type.
    MinSizeRel = "MinSizeRel"

```