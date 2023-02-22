from typing import NamedTuple

class CMakeOptions(NamedTuple):
    """
    Various CMake options that may be enabled via PyMake flags.
    """
    # Whether to pass `--verbose` to CMake.
    verbose: bool
