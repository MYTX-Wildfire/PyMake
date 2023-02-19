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

    def to_string(self) -> str:
        """
        Converts the target type to its string form.
        """
        if self == ETargetType.EXECUTABLE:
            return "Executable"
        elif self == ETargetType.STATIC:
            return "Static"
        elif self == ETargetType.SHARED:
            return "Shared"
        elif self == ETargetType.INTERFACE:
            return "Interface"
        else:
            raise NotImplementedError()
