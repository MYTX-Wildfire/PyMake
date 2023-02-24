
# File cmake\_version.py

[**File List**](files.md) **>** [**common**](dir_3ab6d032c6cf1bbf53e47468d3941a46.md) **>** [**cmake\_version.py**](cmake__version_8py.md)

[Go to the documentation of this file.](cmake__version_8py.md) 

```Python

from enum import Enum

class ECMakeVersion(Enum):
    """
    Defines CMake versions supported by the PyMake transpiler.
    """
    # CMake v3.14.5 (released 2019-05-31)
    V3_14 = "3.14"

    # CMake v3.25.2 (released 2023-01-19)
    V3_25 = "3.25"

```