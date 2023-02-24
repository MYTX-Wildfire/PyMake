
# File cmake\_generator.py

[**File List**](files.md) **>** [**common**](dir_3ab6d032c6cf1bbf53e47468d3941a46.md) **>** [**cmake\_generator.py**](common_2cmake__generator_8py.md)

[Go to the documentation of this file.](common_2cmake__generator_8py.md) 

```Python

from enum import Enum

class ECMakeGenerator(Enum):
    """
    Defines enums for common CMake generators.
    """
    # Ninja build system.
    Ninja = "Ninja"

```