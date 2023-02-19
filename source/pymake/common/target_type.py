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

    def get_default_install_path(self) -> str:
        """
        Gets the path to use as the default install path for the target type.
        @returns A relative path where the target should be installed to.
        """
        if self == ETargetType.EXECUTABLE:
            return "bin"
        elif self == ETargetType.STATIC or self == ETargetType.SHARED:
            return "lib"
        else:
            raise NotImplementedError()
