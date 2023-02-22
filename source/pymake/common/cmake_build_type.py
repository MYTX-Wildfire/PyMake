from enum import Enum

class ECMakeBuildType(Enum):
    """
    Defines constants for each built in CMake build type.
    """
    # Debug build type.
    Debug = "Debug"

    # Release build type.
    Release = "Release"

    # Release with Debug Info build type.
    RelWithDebInfo = "RelWithDebInfo"

    # Minimum Size Release build type.
    MinSizeRel = "MinSizeRel"
