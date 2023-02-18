from enum import IntEnum

class ECMakeVersion(IntEnum):
    """
    Defines CMake versions supported by the PyMake transpiler.
    """
    # CMake v3.25 (released 2022-11-16)
    V3_25 = 325

    def to_version_string(self) -> str:
        """
        Converts the enum to a version string.
        @returns A string containing the CMake version number represented by the
          enum value. The returned version string will be suitable for use with
          `cmake_minimum_required()`.
        """
        if self == ECMakeVersion.V3_25:
            return "3.25"
        else:
            raise RuntimeError("Unknown value.")
