from __future__ import annotations
from pathlib import Path
from pymake.common.cmake_version import ECMakeVersion
from pymake.core.build_script import BuildScript
from pymake.model.project_scope import ProjectScope
from pymake.generators.cmake_generator import CMakeGenerator
from pymake.tracing.caller_info import CallerInfo
from pymake.tracing.caller_info_formatter import ICallerInfoFormatter
from pymake.tracing.shortened_caller_info_formatter import ShortenedCallerInfoFormatter
from pymake.tracing.traced_dict import TracedDict
from typing import Dict, Optional

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
        install_dir: str | Path,
        caller_info_formatter: Optional[ICallerInfoFormatter] = None) \
            -> PyMakeProject:
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
        @param caller_info_formatter The formatter to use when outputting caller
          information. If this is None, a default formatter will be used.
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
            install_dir,
            caller_info_formatter
        )
        PyMakeProject._pymake_projects[origin] = project
        return project


    def __init__(self,
        cmake_version: ECMakeVersion,
        source_dir: str | Path,
        generated_dir: str | Path,
        build_dir: str | Path,
        install_dir: str | Path,
        caller_info_formatter: Optional[ICallerInfoFormatter] = None):
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
        @param caller_info_formatter The formatter to use when outputting caller
          information. If this is None, a default formatter will be used.
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
        if caller_info_formatter:
            self._caller_info_formatter = caller_info_formatter
        else:
            self._caller_info_formatter = ShortenedCallerInfoFormatter(
                source_dir
            )

        # Collection of project scopes
        self._project_scopes: TracedDict[str, ProjectScope] = TracedDict()


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


    def get_or_add_project_scope(self, name: str) -> ProjectScope:
        """
        Gets or adds a project scope to the project.
        @param name Name of the project scope.
        @return The project scope.
        """
        raise NotImplementedError()


    def generate_project(self,
        use_spaces: bool = False,
        tab_size: int = 4) -> None:
        """
        Generates the CMake build scripts for the project.
        @param use_spaces Whether to use spaces instead of tabs for indentation
          in the generated output.
        @param tab_size The number of spaces to use for each indentation level.
          Only used if `use_spaces` is True.
        """
        # Create the top-level build script
        build_script = BuildScript(
            target_path=self.generated_dir / "CMakeLists.txt",
            generator=CMakeGenerator(
                self._caller_info_formatter,
                use_spaces,
                tab_size
            )
        )

        # Generate required initial declarations
        with build_script.generator.open_method_block(
            "cmake_minimum_required") as b:
            b.add_keyword_arguments("VERSION", self._cmake_version.value)

        # Generate add_subdirectory() calls for each project scope
        for project_name, _ in self._project_scopes:
            with build_script.generator.open_method_block(
                "add_subdirectory") as b:
                b.add_arguments(project_name)

        # Write the top-level build script to disk
        build_script.write_file()

        # Generate the build scripts for each project scope
        for project_name, project_scope in self._project_scopes:
            project_dir = self.generated_dir / project_name
            project_dir.mkdir(parents=True, exist_ok=True)

            project_build_script = BuildScript(
                target_path=project_dir / "CMakeLists.txt",
                generator=CMakeGenerator(
                    self._caller_info_formatter,
                    use_spaces,
                    tab_size
                )
            )
            project_scope.generate_project(
                project_dir,
                project_build_script
            )
