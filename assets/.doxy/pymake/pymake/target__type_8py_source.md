
# File target\_type.py

[**File List**](files.md) **>** [**common**](dir_3ab6d032c6cf1bbf53e47468d3941a46.md) **>** [**target\_type.py**](target__type_8py.md)

[Go to the documentation of this file.](target__type_8py.md) 

```Python

from enum import Enum

class ETargetType(Enum):
    """
    Enum for the various CMake target types.
    """
    # Indicates that the target creates an executable binary.
    EXECUTABLE = "Executable"

    # Indicates that the target creates a static library.
    STATIC = "Static"

    # Indicates that the target creates a shared library.
    SHARED = "Shared"

    # Indicates that the target is an interface target.
    INTERFACE = "Interface"

```