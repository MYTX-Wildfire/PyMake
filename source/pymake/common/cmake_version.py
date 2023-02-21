from enum import IntEnum

class ECMakeVersion(IntEnum):
    """
    Defines CMake versions supported by the PyMake transpiler.
    """
    # CMake v3.14.5 (released 2019-05-31)
    V3_14 = 314

    # CMake v3.25.2 (released 2023-01-19)
    V3_25 = 325

    def to_version_string(self) -> str:
        """
        Converts the enum to a version string.
        @returns A string containing the CMake version number represented by the
          enum value. The returned version string will be suitable for use with
          `cmake_minimum_required()`.
        """
        if self == ECMakeVersion.V3_14:
            return "3.14"
        if self == ECMakeVersion.V3_25:
            return "3.25"
        else:
            raise RuntimeError("Unknown value.")
