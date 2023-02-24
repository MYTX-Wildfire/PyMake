
# File scope.py

[**File List**](files.md) **>** [**common**](dir_3ab6d032c6cf1bbf53e47468d3941a46.md) **>** [**scope.py**](scope_8py.md)

[Go to the documentation of this file.](scope_8py.md) 

```Python

from enum import Enum

class EScope(Enum):
    """
    Defines values for each valid CMake scope value.
    """
    # Value for CMake's private visibility scope
    PRIVATE = "PRIVATE"

    # Value for CMake's interface visibility scope
    INTERFACE = "INTERFACE"

    # Value for CMake's public visibility scope
    PUBLIC = "PUBLIC"

```