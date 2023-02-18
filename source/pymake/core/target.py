from abc import ABC
from pymake.common.target_type import ETargetType

class Target(ABC):
    """
    Base type for classes that represent a CMake target.
    """
    def __init__(self,
        target_name: str,
        target_type: ETargetType):
        """
        Initializes the target.
        @param target_name Name of the target.
        @param target_type Type of the target.
        """
        self._target_name = target_name
        self._target_type = target_type
