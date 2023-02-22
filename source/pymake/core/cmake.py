from abc import ABC, abstractmethod
from pathlib import Path
from pymake.common.cmake_version import ECMakeVersion
from pymake.common.project_language import EProjectLanguage
from pymake.core.build_script_set import BuildScriptSet
from pymake.core.preset import Preset
from pymake.core.project import Project
from pymake.tracing.caller_info import CallerInfo
from pymake.tracing.caller_info_formatter import ICallerInfoFormatter
from pymake.tracing.shortened_caller_info_formatter \
    import ShortenedCallerInfoFormatter
from typing import Dict, Iterable, List

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

        # Formatter that should be used when printing tracing info
        self._formatter: ICallerInfoFormatter = \
            ShortenedCallerInfoFormatter(self._source_dir)

        # Project scopes added to the project, indexed by project name
        self._projects: Dict[str, Project] = {}

        # Presets for the project, indexed by preset name
        self._presets: Dict[str, Preset] = {}

        # Presets to use if none are specified
        self._default_presets: List[Preset] = []

        # Build script set to write CMake code to
        self._build_scripts = BuildScriptSet(
            self._source_dir,
            self._generated_dir,
            self._formatter
        )


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
        project = Project(
            self._build_scripts,
            project_name,
            project_languages
        )
        self._projects[project_name] = project
        return project


    def add_preset(self, preset_name: str) -> Preset:
        """
        Adds a preset to the CMake project.
        @param preset_name Name of the preset.
        @throws ValueError Thrown if a preset with the given name already exists.
        """
        # Check if a preset with the given name already exists
        if preset_name in self._presets:
            prev_preset = self._presets[preset_name]
            error_str = f"Error: A preset with the name '{preset_name}' " + \
                "already exists.\n"
            error_str += "Note: The preset was previously added at " + \
                f"'{prev_preset.origin.file_path}':" + \
                f"'{prev_preset.origin.line_number}'"
            raise ValueError(error_str)

        # Add the preset
        preset = Preset(preset_name)
        self._presets[preset_name] = preset
        return preset


    def build(self, generate_first: bool = True) -> None:
        """
        Builds the CMake project.
        @param generate_first If True, the CMake build scripts will be
          generated before building the project.
        """
        if generate_first:
            self.generate()


    def generate(self) -> None:
        """
        Generates the CMake build scripts.
        """
        self._build_scripts.generate()
        self._generate_presets(self._generated_dir / "CMakePresets.json")


    def set_default_presets(self, presets: Preset | Iterable[Preset]):
        """
        Sets the default preset for the CMake project.
        @param presets Preset(s) to set as the default.
        """
        self._default_presets = list(presets) \
            if isinstance(presets, Iterable) else [presets]


    @abstractmethod
    def _generate_presets(self, output_path: Path) -> None:
        """
        Generates the CMakePresets.json file (if supported).
        @param output_path Path where the CMakePresets.json file should be
          written.
        """
        raise NotImplementedError()
