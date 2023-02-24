
# File target.py

[**File List**](files.md) **>** [**core**](dir_b275da0bd59d7f0b7cbb72771801f871.md) **>** [**target.py**](target_8py.md)

[Go to the documentation of this file.](target_8py.md) 

```Python

from __future__ import annotations
from abc import ABC, abstractmethod
from pathlib import Path
from pymake.common.scope import EScope
from pymake.common.target_type import ETargetType
from pymake.core.build_script_set import BuildScriptSet
from pymake.core.scoped_sets import ScopedSets
from pymake.generators.trace_file_generator import ITraceFileGenerator
from pymake.tracing.caller_info import CallerInfo
from pymake.tracing.traced import ITraced, Traced
from typing import Dict, List, Iterable, Optional

class ITarget(ABC, ITraced):
    """
    Represents a single CMake target.
    """
    def __init__(self,
        build_scripts: BuildScriptSet,
        target_name: str,
        target_type: ETargetType):
        """
        Initializes the target.
        @param build_scripts Set of build scripts that the project will generate.
        @param target_name Name of the target.
        @param target_type Type of the target.
        """
        super().__init__()
        self._build_scripts_build_scripts = build_scripts
        self._target_name_target_name = target_name
        self._target_type_target_type = target_type
        self._is_full_target_is_full_target = False

        # Properties for the target
        # Note that each of these collections does *not* include values that
        #   were added to targets that this target links to. To get a target
        #   instance with all values, use the `get_full_target()` method.
        self._sources: ScopedSets[Path] = ScopedSets()

        # Whether the target will be installed
        # If `_is_installed` is `True` but `_install_path` is `None`, the path
        #   that the target will be installed to will be CMake's default path
        #   for the target type.
        self._is_installed_is_installed = False
        self._install_path_install_path: Optional[Traced[str]] = None


    @property
    def is_installed(self) -> bool:
        """
        Gets whether the target will be installed.
        """
        return self._is_installed_is_installed


    @property
    def install_path(self) -> Optional[str]:
        """
        Gets the path that the target will be installed to.
        """
        return self._install_path_install_path.value if self._install_path_install_path else None


    @property
    def is_full_target(self) -> bool:
        """
        Gets whether the target includes all values from targets that it links to.
        """
        return self._is_full_target_is_full_target


    @property
    def target_name(self) -> str:
        """
        Gets the name of the target.
        """
        return self._target_name_target_name


    @property
    def target_type(self) -> ETargetType:
        """
        Gets the type of the target.
        """
        return self._target_type_target_type


    @property
    def sources(self) -> ScopedSets[Path]:
        """
        Gets the source files for the target.
        """
        return self._sources


    def add_sources(self,
        sources: str | Iterable[str],
        scope: EScope = EScope.PRIVATE) -> None:
        """
        Adds source files to the target.
        @param sources Source files to add to the target. If any path is a
          relative path, it will be interpreted relative to the caller's
          directory.
        @param scope Scope of the source files.
        """
        if isinstance(sources, str):
            sources = [sources]

        # Get the path of the caller
        # Any relative paths will be interpreted relative to this path.
        caller_info = CallerInfo.closest_external_frame()
        caller_path = Path(caller_info.file_path).parent

        source_abs_paths: List[str] = []
        for source in sources:
            # Convert all paths to absolute paths if they aren't already
            path = Path(source)
            if not path.is_absolute():
                path = caller_path / path

            self._sources.select_set(scope).add(path)
            source_abs_paths.append(str(path))

        # Generate the CMake code
        generator = self._build_scripts_build_scripts.get_or_add_build_script().generator
        with generator.open_method_block("target_sources") as b:
            b.add_arguments(self._target_name_target_name)
            b.add_keyword_arguments(
                scope.value,
                source_abs_paths
            )


    def generate_trace_file(self,
        output_path: Path,
        generator: ITraceFileGenerator):
        """
        Generates a trace file for the target.
        @param output_path Path to the output file.
        @param generator Generator to create the trace file using.
        """
        # Generate a dictionary containing the properties to write to the trace
        #   file
        full_target = self.get_full_targetget_full_target()
        props: Dict[str, object] = {}
        props["type"] = full_target._target_type.value
        props["sources"] = full_target._sources.to_trace_dict()
        props["is_installed"] = full_target._is_installed
        props["install_path"] = full_target._install_path.value \
            if full_target._install_path else "<cmake_default>"

        generator.write_file({
            self.target_nametarget_name: props
        }, output_path)


    @abstractmethod
    def get_full_target(self) -> ITarget:
        """
        Gets a target instance that includes all values for the target.
        Target instances normally do not include values from targets that
          they link to. The target instance returned by this method contains
          all values for the target, including values from linked-to targets.
        @returns A target instance that includes all values from targets that
          this target links to.
        """
        raise NotImplementedError()


    def install(self,
        install_path: Optional[str] = None) -> None:
        """
        Installs the target.
        @param install_path Path to install the target to. If this is `None`,
          the path that the target will be installed to will be CMake's default
          path for the target type.
        """
        self._is_installed_is_installed = True
        if install_path:
            self._install_path_install_path = Traced(install_path)

        # Generate the CMake code
        generator = self._build_scripts_build_scripts.get_or_add_build_script().generator
        with generator.open_method_block("install") as b:
            b.add_keyword_arguments(
                "TARGETS",
                self._target_name_target_name
            )
            if self._install_path_install_path:
                b.add_keyword_arguments(
                    "DESTINATION",
                    self._install_path_install_path.value
                )

```