from abc import ABC
from pathlib import Path
from pymake.common.cmake_version import ECMakeVersion
from pymake.common.project_language import EProjectLanguage
from pymake.core.project import Project
from pymake.tracing.caller_info import CallerInfo
from typing import Dict, Iterable

class ICMake(ABC):
    """
    Represents a single PyMake-based CMake project.
    """
    def __init__(self,
        minimum_version: ECMakeVersion,
        source_directory: str | Path,
        generated_directory: str | Path):
        """
        Initializes the CMake project.
        @param minimum_version Minimum CMake version required to build the
          project.
        @param source_directory Path to the directory containing the source
          files for the PyMake project. If this is a relative path, it will be
          interpreted relative to the caller's directory.
        @param generated_directory Path to the directory where PyMake should
          generate the CMake files. If this is a relative path, it will be
          interpreted relative to the caller's directory.
        """
        self._minimum_version = minimum_version

        # Get the path to the caller's directory
        caller_info = CallerInfo.closest_external_frame()
        caller_dir = Path(caller_info.file_path).parent

        # Get absolute paths to each directory
        source_directory = Path(source_directory) \
            if isinstance(source_directory, str) else source_directory
        generated_directory = Path(generated_directory) \
            if isinstance(generated_directory, str) else generated_directory

        if not source_directory.is_absolute():
            source_directory = caller_dir / source_directory
        if not generated_directory.is_absolute():
            generated_directory = caller_dir / generated_directory

        self._source_dir = source_directory
        self._generated_dir = generated_directory

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
