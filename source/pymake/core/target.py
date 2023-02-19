from abc import ABC
from pathlib import Path
from pymake.common.scope import EScope
from pymake.common.target_type import ETargetType
from pymake.core.project_state import ProjectState
from pymake.generation.basic_generator import BasicGenerator
from pymake.helpers.code_generator import CodeGenerator
from pymake.helpers.path_statics import to_abs_path
from pymake.helpers.yaml_generator import YamlGenerator
from pymake.tracing.caller_info import CallerInfo
from pymake.tracing.traced import Traced
from pymake.tracing.traced_set import TracedSet
from typing import Iterable, Optional

class Target(ABC):
    """
    Base type for classes that represent a CMake target.
    """
    def __init__(self,
        project_state: ProjectState,
        target_name: str,
        target_type: ETargetType):
        """
        Initializes the target.
        @param project_state State information for the PyMake project that the
          target is part of.
        @param target_name Name of the target.
        @param target_type Type of the target.
        @throws ValueError Thrown if any parameter is invalid.
        """
        # Validate method arguments
        if not target_name:
            raise ValueError("A project name string may not be empty.")
        elif target_name.isspace():
            raise ValueError("A project's name cannot be only whitespace.")

        self._project_state = project_state
        self._target_name = Traced(target_name)
        self._target_type = target_type

        # Track tracing information for each target property
        self._install_path: Optional[Traced[str]] = None

        # Set of all source files to use when compiling the target
        # Each path will be an absolute path with all symlinks resolved.
        self._sources: TracedSet[Path] = TracedSet()

    @property
    def target_name(self) -> str:
        """
        Gets the name of the target.
        """
        return self._target_name.value

    def add_sources(self,
        sources: str | Iterable[str],
        scope: EScope = EScope.PRIVATE) -> None:
        """
        Adds one or more sources to the target.
        @param sources Sources to add to the target. Paths may be relative or
          absolute paths. If a relative path is provided, the path will be
          interpreted relative to the path of the build script invoking this
          method.
        @param scope Scope to use for the sources.
        @throws ValueError Thrown if a source has already been added previously.
        """
        if isinstance(sources, str):
            sources = [sources]

        # Get info about the build script adding the sources
        call_site = CallerInfo(1)

        # Convert each path to an absolute path
        source_paths = [
            to_abs_path(Path(p), call_site.file_path.parent) for p in sources
        ]
        for p in source_paths:
            self._sources.add(p)

        # Generate the CMake code for adding the source(s) to the target
        generator = CodeGenerator()
        generator.open_method("target_sources")
        generator.write_method_parameter(None, self._target_name.value)
        generator.write_method_parameter(
            scope.to_cmake_string(),
            [str(p) for p in source_paths]
        )
        generator.close_method()

        # Add the generated CMake code
        build_script = self._project_state.get_or_add_build_script()
        build_script.add_generator(BasicGenerator(
            generator.code
        ))

    def install(self, path: Optional[str] = None) -> None:
        """
        Generates an install command for the target.
        @param path Path to install the target to. If this is a relative path,
          it will be interpreted relative to CMake's install prefix. If this is
          not provided, the default location for the target type will be used.
        """
        if not path:
            path = self._target_type.get_default_install_path()
        self._install_path = Traced(path)

        # Generate the CMake code
        generator = CodeGenerator()
        generator.open_method("install")
        generator.write_method_parameter(
            "TARGETS",
            self._target_name.value
        )
        generator.write_method_parameter(
            "DESTINATION",
            path
        )
        generator.close_method()

        # Add the code to the build script
        build_script = self._project_state.get_or_add_build_script()
        build_script.add_generator(BasicGenerator(
            generator.code
        ))

    def to_yaml(self) -> str:
        """
        Converts the preset into a YAML file.
        @returns A string containing the contents of the YAML file.
        """
        generator = YamlGenerator()
        generator.open_block(self._target_name.value)

        # Write general properties
        generator.write_traced("Target name", self._target_name)
        generator.write_block_pair(
            "Target type",
            self._target_type.to_string(),
            add_quotes=False
        )

        # Write optional properties
        if self._install_path:
            generator.write_block_pair("Installed", "yes", add_quotes=False)
            generator.write_traced("Install path", self._install_path)
        else:
            generator.write_block_pair("Installed", "no", add_quotes=False)

        # Write target sources
        if self._sources:
            generator.open_block("Sources")
            for path in self._sources:
                generator.write_traced("file", path)
            generator.close_block()
        else:
            generator.write_empty_dict("Sources")

        return generator.text
