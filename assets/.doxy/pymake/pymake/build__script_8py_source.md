
# File build\_script.py

[**File List**](files.md) **>** [**core**](dir_b275da0bd59d7f0b7cbb72771801f871.md) **>** [**build\_script.py**](build__script_8py.md)

[Go to the documentation of this file.](build__script_8py.md) 

```Python

from pathlib import Path
from pymake.generators.cmake_generator import CMakeGenerator
from typing import NamedTuple

class BuildScript(NamedTuple):
    """
    Stores all data for a CMake build script that must be generated.
    """
    # Path that the build script should be generated at.
    # @invariant This will be an absolute path.
    target_path: Path

    # Generator to use to add CMake code to the build script.
    generator: CMakeGenerator

```