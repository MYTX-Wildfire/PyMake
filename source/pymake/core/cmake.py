from abc import ABC
from pymake.common.cmake_version import ECMakeVersion
from pymake.core.project import Project
from typing import Dict

class ICMake(ABC):
    """
    Represents a single PyMake-based CMake project.
    """
    def __init__(self,
        minimum_version: ECMakeVersion):
        """
        Initializes the CMake project.
        @param minimum_version Minimum CMake version required to build the
          project.
        """
        self._minimum_version = minimum_version

        # Project scopes added to the project, indexed by project name
        self._projects: Dict[str, Project] = {}
