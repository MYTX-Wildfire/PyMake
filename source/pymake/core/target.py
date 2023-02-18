from abc import ABC
from pymake.common.target_type import ETargetType
from pymake.core.project_state import ProjectState
from pymake.helpers.caller_info import CallerInfo

class Target(ABC):
    """
    Base type for classes that represent a CMake target.
    """
    def __init__(self,
        project_state: ProjectState,
        target_name: str,
        target_type: ETargetType,
        caller_offset: int):
        """
        Initializes the target.
        @param project_state State information for the PyMake project that the
          target is part of.
        @param target_name Name of the target.
        @param target_type Type of the target.
        @param caller_offset Number of stack frames to traverse to get to
          the stack frame of the pymake build script.
        @throws ValueError Thrown if any parameter is invalid.
        """
        # Validate method arguments
        if not target_name:
            raise ValueError("A project name string may not be empty.")
        elif target_name.isspace():
            raise ValueError("A project's name cannot be only whitespace.")

        self._project_state = project_state
        self._target_name = target_name
        self._target_type = target_type
        self._call_site = CallerInfo(caller_offset + 1)
