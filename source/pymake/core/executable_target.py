from __future__ import annotations
from pymake.common.target_type import ETargetType
from pymake.core.target import ITarget

class ExecutableTarget(ITarget):
    """
    Represents a single executable CMake target.
    """
    def __init__(self,
        target_name: str):
        """
        Initializes the target.
        @param target_name Name of the target.
        """
        super().__init__(target_name, ETargetType.EXECUTABLE)


    def get_full_target(self) -> ExecutableTarget:
        """
        Gets a target instance that includes all values for the target.
        Target instances normally do not include values from targets that
          they link to. The target instance returned by this method contains
          all values for the target, including values from linked-to targets.
        @returns A target instance that includes all values from targets that
          this target links to.
        """
        raise NotImplementedError()
