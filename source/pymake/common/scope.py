from enum import IntEnum

class EScope(IntEnum):
    """
    Defines values for each valid CMake scope value.
    """
    # Value for CMake's private visibility scope
    PRIVATE = 0

    # Value for CMake's interface visibility scope
    INTERFACE = 1

    # Value for CMake's public visibility scope
    PUBLIC = 2

    def to_cmake_string(self) -> str:
        """
        Converts the enum to the equivalent CMake string.
        @returns A string containing the equivalent CMake text. This string is
           suitable for use in methods such as `target_link_libraries()`,
           `target_sources()`, etc.
        """
        if self == EScope.PUBLIC:
            return "PUBLIC"
        elif self == EScope.INTERFACE:
            return "INTERFACE"
        elif self == EScope.PRIVATE:
            return "PRIVATE"
        else:
            raise RuntimeError("Unknown value.")

