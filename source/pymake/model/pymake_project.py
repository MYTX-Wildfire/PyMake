from __future__ import annotations
from pathlib import Path
from pymake.common.cmake_version import ECMakeVersion
from pymake.model.project_scope import ProjectScope
from pymake.tracing.caller_info import CallerInfo
from pymake.tracing.traced_dict import TracedDict
from typing import Dict, Iterable

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
        origin: CallerInfo | None,
        cmake_version: ECMakeVersion,
        source_dir: str | Path,
        generated_dir: str | Path,
        build_dir: str | Path,
        install_dir: str | Path) -> PyMakeProject:
        """
        Gets or creates the PyMake project for the target origin.
        @param origin Location in external PyMake build scripts to get the
          PyMake project for. If this is None, the closest external frame will
          be used.
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

        # Collection of project scopes
        self._project_scopes: TracedDict[str, ProjectScope] = TracedDict()


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


    def get_or_add_project_scope(self, name: str) -> ProjectScope:
        """
        Gets or adds a project scope to the project.
        @param name Name of the project scope.
        @return The project scope.
        """
        raise NotImplementedError()
