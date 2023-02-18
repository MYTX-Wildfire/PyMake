from abc import ABC
from pathlib import Path
from pymake.common.scope import EScope
from pymake.common.target_type import ETargetType
from pymake.core.project_state import ProjectState
from pymake.helpers.caller_info import CallerInfo
from pymake.helpers.path_statics import to_abs_path
from pymake.generation.basic_generator import BasicGenerator
from typing import Dict, Iterable

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

        # Keep track of where each source was added from
        # This is used to improve debugging when stepping through PyMake build
        #   scripts but is not needed for code generation since call site
        #   information is written out when the CMake code is generated. Each
        #   source file's path will be stored as an absolute path regardless of
        #   how the file was referenced originally.
        self._sources: Dict[Path, CallerInfo] = {}

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
        @throws ValueError Thrown if
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
            # TODO: If strict checks are enabled, raise an error if a source
            #   path has already been added before
            self._sources[p] = call_site

        # Generate the CMake code for adding the source(s) to the target
        code = "target_sources(\n"
        code += "\t" + self._target_name + "\n"
        code += "\t" + scope.to_cmake_string() + "\n"
        for p in source_paths:
            code += f"\t\t{p}\n"
        code += ")"

        build_script = self._project_state.get_or_add_build_script(1)
        build_script.add_generator(BasicGenerator(
            code,
            caller_offset=1
        ))
