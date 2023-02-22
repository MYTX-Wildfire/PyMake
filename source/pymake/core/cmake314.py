from pymake.common.cmake_version import ECMakeVersion
from pymake.core.cmake import ICMake

class CMake314(ICMake):
    """
    ICMake implementation that generates CMake v3.14-compliant code.
    """
    def __init__(self):
        """
        Initializes the CMake instance.
        """
        super().__init__(ECMakeVersion.V3_14)
