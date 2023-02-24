
# File cmake\_options.py

[**File List**](files.md) **>** [**core**](dir_b275da0bd59d7f0b7cbb72771801f871.md) **>** [**cmake\_options.py**](cmake__options_8py.md)

[Go to the documentation of this file.](cmake__options_8py.md) 

```Python

from typing import NamedTuple

class CMakeOptions(NamedTuple):
    """
    Various CMake options that may be enabled via PyMake flags.
    """
    # Whether to pass `--verbose` to CMake.
    verbose: bool

```