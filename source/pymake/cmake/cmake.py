from abc import ABC, abstractmethod
from pymake.model.pymake_project import PyMakeProject
from pymake.model.preset import Preset
from typing import List

class ICMake(ABC):
    """
    Base type for classes that handle version-specific CMake behavior.
    """
    @abstractmethod
    def configure(self,
        project: PyMakeProject,
        presets: List[Preset]) -> int:
        """
        Runs the CMake configure step on the project.
        @param project The project to configure.
        @param presets The preset(s) to configure CMake to use. Must contain at
          least one element.
        @return The exit code of the CMake configure step.
        """
        raise NotImplementedError()


    @abstractmethod
    def build(self,
        project: PyMakeProject,
        presets: List[Preset]) -> int:
        """
        Runs the CMake build step on the project.
        @param project The project to build.
        @param presets The preset(s) to build. Must contain at least one element.
        @return The exit code of the CMake build step.
        """
        raise NotImplementedError()
