from enum import Enum

class ETargetType(Enum):
    """
    Enum for the various CMake target types.
    """
    ## Indicates that the target creates an executable binary.
    EXECUTABLE = "Executable"

    ## Indicates that the target creates a static library.
    STATIC = "Static"

    ## Indicates that the target creates a shared library.
    SHARED = "Shared"

    ## Indicates that the target is an interface target.
    INTERFACE = "Interface"
