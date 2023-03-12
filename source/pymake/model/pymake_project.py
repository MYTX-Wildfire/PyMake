from __future__ import annotations
from pathlib import Path
from pymake.common.cmake_version import ECMakeVersion
from pymake.common.project_language import EProjectLanguage
from pymake.model.preset import Preset
from pymake.model.project_scope import ProjectScope
from pymake.tracing.caller_info import CallerInfo
from pymake.tracing.traced_dict import TracedDict
from typing import Dict, List, Iterable

class PyMakeProject:
    """
    Stores all state information for a PyMake project.
    """
    # PyMake projects that have been created.
    # Each project is indexed by the location in external PyMake build scripts
    #   that created the project.
    _pymake_projects: Dict[CallerInfo, PyMakeProject] = {}

    @staticmethod
    def get_pymake_project_by_origin(
        cmake_version: ECMakeVersion,
        source_dir: str | Path,
        generated_dir: str | Path,
        build_dir: str | Path,
        install_dir: str | Path,
        origin: CallerInfo | None = None) -> PyMakeProject:
        """
        Gets or creates the PyMake project for the target origin.
        @param cmake_version The version of CMake to target when generating the
          project.
        @param source_dir The path to the folder containing all source files.
          This path must be to the root of the source directory and may be an
          absolute or relative path. If the path is a relative path, it will be
          resolved relative to the caller's directory.
        @param generated_dir The path to the folder where PyMake will generate
          CMake files in. This may be an absolute or relative path. If the path
          is a relative path, it will be resolved relative to the caller's
          directory.
        @param build_dir The path to the folder that CMake will use as its build
          tree. This may be an absolute or relative path. If the path is a
          relative path, it will be resolved relative to the caller's directory.
        @param install_dir The path to the folder that CMake will use as its
          install tree. This may be an absolute or relative path. If the path
          is a relative path, it will be resolved relative to the caller's
          directory.
        @param origin Location in external PyMake build scripts to get the
          PyMake project for. If this is None, the closest external frame will
          be used.
        @returns The PyMake project for the call site.
        """
        if not origin:
            origin = CallerInfo.closest_external_frame()

        # Check if a project has already been created for the origin.
        if origin in PyMakeProject._pymake_projects:
            return PyMakeProject._pymake_projects[origin]

        # Create a new project for the origin.
        project = PyMakeProject(
            cmake_version,
            source_dir,
            generated_dir,
            build_dir,
            install_dir
        )
        PyMakeProject._pymake_projects[origin] = project
        return project


    def __init__(self,
        cmake_version: ECMakeVersion,
        source_dir: str | Path,
        generated_dir: str | Path,
        build_dir: str | Path,
        install_dir: str | Path):
        """
        Initializes the project.
        @param cmake_version The version of CMake to target when generating the
          project.
        @param source_dir The path to the folder containing all source files.
          This path must be to the root of the source directory and may be an
          absolute or relative path. If the path is a relative path, it will be
          resolved relative to the caller's directory.
        @param generated_dir The path to the folder where PyMake will generate
          CMake files in. This may be an absolute or relative path. If the path
          is a relative path, it will be resolved relative to the caller's
          directory.
        @param build_dir The path to the folder that CMake will use as its build
          tree. This may be an absolute or relative path. If the path is a
          relative path, it will be resolved relative to the caller's directory.
        @param install_dir The path to the folder that CMake will use as its
          install tree. This may be an absolute or relative path. If the path
          is a relative path, it will be resolved relative to the caller's
          directory.
        """
        # Get the path to resolve relative paths against.
        caller_info = CallerInfo.closest_external_frame()
        caller_dir = caller_info.file_path.parent

        # Convert each input path to a path object
        if isinstance(source_dir, str):
            source_dir = Path(source_dir)
        if isinstance(generated_dir, str):
            generated_dir = Path(generated_dir)
        if isinstance(build_dir, str):
            build_dir = Path(build_dir)
        if isinstance(install_dir, str):
            install_dir = Path(install_dir)

        # Convert all input paths to absolute paths
        if not source_dir.is_absolute():
            source_dir = caller_dir / source_dir
        if not generated_dir.is_absolute():
            generated_dir = caller_dir / generated_dir
        if not build_dir.is_absolute():
            build_dir = caller_dir / build_dir
        if not install_dir.is_absolute():
            install_dir = caller_dir / install_dir

        # Store input parameters
        self._cmake_version = cmake_version
        self._source_dir = source_dir
        self._generated_dir = generated_dir
        self._build_dir = build_dir
        self._install_dir = install_dir

        # Collection of project scopes, indexed by project name.
        self._project_scopes: TracedDict[str, ProjectScope] = TracedDict()

        # Collection of presets, indexed by preset name.
        self._presets: TracedDict[str, Preset] = TracedDict()

        # Preset(s) to use if no preset was specified on the command line.
        self._default_presets: List[Preset] = []


    @property
    def cmake_version(self) -> ECMakeVersion:
        """
        The version of CMake to target when generating the project.
        """
        return self._cmake_version


    @property
    def source_dir(self) -> Path:
        """
        The path to the folder containing all source files.
        This is guaranteed to be an absolute path.
        """
        return self._source_dir


    @property
    def generated_dir(self) -> Path:
        """
        The path to the folder where PyMake will generate CMake files in.
        This is guaranteed to be an absolute path.
        """
        return self._generated_dir


    @property
    def build_dir(self) -> Path:
        """
        The path to the folder that CMake will use as its build tree.
        This is guaranteed to be an absolute path.
        """
        return self._build_dir


    @property
    def install_dir(self) -> Path:
        """
        The path to the folder that CMake will use as its install tree.
        This is guaranteed to be an absolute path.
        """
        return self._install_dir


    @property
    def project_scopes(self) -> Iterable[ProjectScope]:
        """
        The project scopes in the project.
        """
        return [p for _, p in self._project_scopes]


    @property
    def presets(self) -> Iterable[Preset]:
        """
        The presets in the project.
        """
        return [p for _, p in self._presets]


    @property
    def default_presets(self) -> Iterable[Preset]:
        """
        The preset(s) to use if no preset was specified on the command line.
        """
        return self._default_presets


    def add_preset(self, preset_name: str) -> Preset:
        """
        Adds a preset to the project.
        @param preset_name The name of the preset.
        @throws RuntimeError Thrown if the preset already exists with the same
          name and was declared at a different location.
        @return A newly created preset or the previously created preset.
        """
        preset = Preset(preset_name)

        # Check if the preset already exists.
        if preset_name in self._presets:
            # If the preset already exists, check if it was declared at the
            #   same location. If it was, return the existing preset and don't
            #   throw an exception.
            prev_preset = self._presets[preset_name]
            if prev_preset.origin == preset.origin:
                return prev_preset

            error_str = "Error: Cannot add a preset with the name " + \
                f"'{preset_name}'."
            error_str = "Note: A preset with the name " + \
                f"'{preset_name}' already exists in the PyMake project."
            error_str = "    The preset was previously added at " + \
                f"{prev_preset.origin.file_path}:" + \
                f"{prev_preset.origin.line_number}."
            error_str = "    The new preset is being added at " + \
                f"{preset.origin.file_path}:" + \
                f"{preset.origin.line_number}."
            raise RuntimeError(error_str)

        # Add the preset to the project.
        self._presets[preset_name] = preset
        return preset


    def add_project_scope(self,
        project_name: str,
        project_languages: EProjectLanguage | Iterable[EProjectLanguage],
        project_all_target_name: str,
        project_test_target_name: str) -> ProjectScope:
        """
        Adds a project scope to the project.
        @param project_name The name of the project.
        @param project_languages The languages used in the project.
        @param enable_ctest Whether to enable CTest for the project.
        @param project_all_target_name Name of the project-specific `all`
          target.
        @param project_test_target_name Name of the project-specific `test`
          target.
        @throws RuntimeError Thrown if the project scope already exists with the
          same name and was declared at a different location.
        @return A newly created project scope or the previously created project
          scope.
        """
        project = ProjectScope(
            project_name,
            project_languages,
            project_all_target_name,
            project_test_target_name
        )

        # Check if the project scope already exists
        if project_name in self._project_scopes:
            # If the previous project scope was declared at the same location,
            #   return it instead of creating a new one or throwing an error.
            prev_project = self._project_scopes[project_name]
            if prev_project.origin == project.origin:
                return prev_project

            error_str = "Error: Cannot add a target with the name " + \
                f"'{project_name}'."
            error_str = "Note: A project scope with the name " + \
                f"'{project_name}' already exists in the PyMake project."
            error_str = "    The project scope was previously added at " + \
                f"{prev_project.origin.file_path}:" + \
                f"{prev_project.origin.line_number}."
            error_str = "    The new project scope is being added at " + \
                f"{project.origin.file_path}:" + \
                f"{project.origin.line_number}."
            raise RuntimeError(error_str)

        # Add the project scope to the project.
        self._project_scopes[project_name] = project
        return project


    def set_default_presets(self, preset: Preset | Iterable[Preset]):
        """
        Sets the default presets for the project.
        @param preset The default preset or presets.
        """
        if isinstance(preset, Preset):
            self._default_presets = [preset]
        else:
            self._default_presets = list(preset)
