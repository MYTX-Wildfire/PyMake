from abc import ABC
from pymake.common.cmake_version import ECMakeVersion
from pymake.common.project_language import EProjectLanguage
from pymake.core.project import Project
from typing import Dict, Iterable

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


    def add_project(self,
        project_name: str,
        project_languages: EProjectLanguage | Iterable[EProjectLanguage]) -> Project:
        """
        Adds a project scope to the CMake project.
        @param project_name Name of the project.
        @param project_languages Languages used in the project.
        @throws ValueError Thrown if a project with the given name already exists.
        @returns The project instance.
        """
        # Check if a project with the given name already exists
        if project_name in self._projects:
            prev_project = self._projects[project_name]
            error_str = f"Error: A project with the name '{project_name}' " + \
                "already exists.\n"
            error_str += "Note: The project was previously added at " + \
                f"'{prev_project.origin.file_path}':" + \
                f"'{prev_project.origin.line_number}'"
            raise ValueError(error_str)

        # Add the project
        project = Project(project_name, project_languages)
        self._projects[project_name] = project
        return project
