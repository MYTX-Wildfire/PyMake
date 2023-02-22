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
