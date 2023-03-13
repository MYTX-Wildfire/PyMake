from enum import Enum

class ETargetType(Enum):
    """
    Enum for the various CMake target types.
    """
    ## Indicates that the target creates an executable binary.
    EXECUTABLE = "EXECUTABLE"

    ## Indicates that the target creates a static library.
    STATIC = "STATIC"

    ## Indicates that the target creates a shared library.
    SHARED = "SHARED"

    ## Indicates that the target is an interface target.
    INTERFACE = "INTERFACE"
