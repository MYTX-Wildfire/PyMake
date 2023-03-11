from __future__ import annotations
from pymake.common.test_flags import ETestFlags
from pymake.tracing.traced import ITraced

class Target(ITraced):
    """
    Represents a CMake target within a PyMake project.
    """
    def __init__(self,
        target_name: str,
        test_flags: int,
        sanitizer_flags: int):
        """
        Initializes the target.
        @param target_name The name of the target.
        @param test_flags Identifies whether the target is a test target and
          what kind of target the test target is.
        @param sanitizer_flags The sanitizers enabled for the target.
        """
        self._target_name = target_name
        self._test_flags = test_flags
        self._sanitizer_flags = sanitizer_flags


    @property
    def target_name(self) -> str:
        """
        Gets the name of the target.
        """
        return self._target_name


    @property
    def test_flags(self) -> int:
        """
        Gets the test flags for the target.
        """
        return self._test_flags


    @property
    def is_test_target(self) -> bool:
        """
        Gets whether the target is a test target.
        """
        return self._test_flags != ETestFlags.NONE


    @property
    def sanitizer_flags(self) -> int:
        """
        Gets the sanitizers enabled for the target.
        """
        return self._sanitizer_flags