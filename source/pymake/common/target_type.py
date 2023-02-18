from enum import IntEnum

class ETargetType(IntEnum):
    """
    Enum for the various CMake target types.
    """
    # Indicates that the target creates an executable binary.
    EXECUTABLE = 0

    # Indicates that the target creates a static library.
    STATIC = 1

    # Indicates that the target creates a shared library.
    SHARED = 2

    # Indicates that the target is an interface target.
    INTERFACE = 3
