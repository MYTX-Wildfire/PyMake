from __future__ import annotations
from pymake.common.target_type import ETargetType
from pymake.model.targets.target import Target

class BuildTarget(Target):
    """
    Represents a target that must be built by CMake.
    """
    def __init__(self,
        target_name: str,
        target_type: ETargetType,
        test_flags: int,
        sanitizer_flags: int):
        """
        Initializes the target.
        @param target_name The name of the target.
        @param target_type The type of the target.
        @param test_flags Identifies whether the target is a test target and
          what kind of target the test target is.
        @param sanitizer_flags The sanitizers enabled for the target.
        """
        super().__init__(
            target_name,
            test_flags,
            sanitizer_flags
        )
        self._target_type = target_type


    @property
    def target_type(self) -> ETargetType:
        """
        Gets the type of the target.
        """
        return self._target_type
