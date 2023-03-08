from __future__ import annotations
from abc import ABC
from pathlib import Path
from pymake.common.scope import EScope
from pymake.common.target_type import ETargetType
from pymake.core.build_script_set import BuildScriptSet
from pymake.core.scoped_sets import ScopedSets
from pymake.generators.trace_file_generator import ITraceFileGenerator
from pymake.tracing.caller_info import CallerInfo
from pymake.tracing.traced import ITraced, Traced
from pymake.util.platform_statics import PlatformStatics
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
        self._build_scripts = build_scripts
        self._target_name = target_name
        self._target_type = target_type
        self._is_full_target = False

        # Properties for the target
        # Note that each of these collections does *not* include values that
        #   were added to targets that this target links to. To get a target
        #   instance with all values, use the `get_full_target()` method.
        self._sources: ScopedSets[Path] = ScopedSets()

        # Include directories to add to the target
        # All paths will be absolute paths.
        self._include_directories: ScopedSets[Path] = ScopedSets()

        # Libraries to link to
        # Each item may be a string containing the name or path to an external
        #   library or a PyMake target. If the item is a PyMake target, the
        #   target will not be an executable target.
        self._link_libraries: ScopedSets[str | ITarget] = ScopedSets()

        # Whether the target will be installed
        # If `_is_installed` is `True` but `_install_path` is `None`, the path
        #   that the target will be installed to will be CMake's default path
        #   for the target type.
        self._is_installed = False
        self._install_path: Optional[Traced[str]] = None


    def __str__(self) -> str:
        """
        Gets a string representation of the target.
        """
        return self._target_name


    @property
    def is_installed(self) -> bool:
        """
        Gets whether the target will be installed.
        """
        return self._is_installed


    @property
    def install_path(self) -> Optional[str]:
        """
        Gets the path that the target will be installed to.
        """
        return self._install_path.value if self._install_path else None


    @property
    def is_full_target(self) -> bool:
        """
        Gets whether the target includes all values from targets that it links to.
        """
        return self._is_full_target


    @property
    def target_name(self) -> str:
        """
        Gets the name of the target.
        """
        return self._target_name


    @property
    def target_type(self) -> ETargetType:
        """
        Gets the type of the target.
        """
        return self._target_type


    @property
    def sources(self) -> ScopedSets[Path]:
        """
        Gets the source files for the target.
        """
        return self._sources


    @property
    def include_directories(self) -> ScopedSets[Path]:
        """
        Gets the include directories for the target.
        """
        return self._include_directories


    @property
    def link_libraries(self) -> ScopedSets[str | ITarget]:
        """
        Gets the libraries that the target will link to.
        """
        return self._link_libraries


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
            path = path.resolve()

            # Only add the path if it hasn't already been added
            if not self._sources.select_set(scope).add(path):
                continue
            source_abs_paths.append(str(path))

        # If no new paths were added, skip generating the CMake code
        if not source_abs_paths:
            return

        # Generate the CMake code
        generator = self._build_scripts.get_or_add_build_script().generator
        with generator.open_method_block("target_sources") as b:
            b.add_arguments(self._target_name)
            b.add_keyword_arguments(
                scope.value,
                source_abs_paths
            )


    def add_include_directories(self,
        include_directories: str | Iterable[str],
        scope: EScope = EScope.PRIVATE) -> None:
        """
        Adds include directories to the target.
        @param include_directories Include directories to add to the target.
          If any path is a relative path, it will be interpreted relative to the
          caller's directory.
        @param scope Scope of the include directories.
        """
        if isinstance(include_directories, str):
            include_directories = [include_directories]

        # Get the path of the caller
        # Any relative paths will be interpreted relative to this path.
        caller_info = CallerInfo.closest_external_frame()
        caller_path = Path(caller_info.file_path).parent

        include_directory_abs_paths: List[str] = []
        for include_directory in include_directories:
            # Convert all paths to absolute paths if they aren't already
            path = Path(include_directory)
            if not path.is_absolute():
                path = caller_path / path
            path = path.resolve()

            if not self._include_directories.select_set(scope).add(path):
                continue
            include_directory_abs_paths.append(str(path))

        # If no new paths were added, skip generating the CMake code
        if not include_directory_abs_paths:
            return

        # Generate the CMake code
        generator = self._build_scripts.get_or_add_build_script().generator
        with generator.open_method_block("target_include_directories") as b:
            b.add_arguments(self._target_name)
            b.add_keyword_arguments(
                scope.value,
                include_directory_abs_paths
            )


    def link_to_target(self,
        target: ITarget,
        scope: EScope = EScope.PRIVATE):
        """
        Configures the current target to link to the target or library.
        @param target Target to link to. Must not be an executable target.
        @param scope Visibility scope for the library.
        """
        # If the target has already been added, don't generate new CMake code
        if not self._link_libraries.select_set(scope).add(target):
            return

        # Generate the CMake code
        generator = self._build_scripts.get_or_add_build_script().generator
        with generator.open_method_block("target_link_libraries") as b:
            b.add_arguments(self._target_name)
            b.add_keyword_arguments(
                scope.value,
                target.target_name
            )


    def link_to_library(self,
        library: str | Path,
        is_static: bool = False,
        is_shared: bool = False,
        scope: EScope = EScope.PRIVATE):
        """
        Configures the current target to link to the library.
        @param library Name or path to the library.
        @param is_static Whether the library is a static library. If this is set
          to true, the platform-specific static library prefix and suffix will
          be added to the library name. Setting this to `True` requires that the
          library name is a string, not a Path.
        @param is_shared Whether the library is a shared library. If this is set
          to true, the platform-specific shared library prefix and suffix will
          be added to the library name.
        @param scope Visibility scope for the library.
        """
        # Add the platform-specific library prefix and suffix if necessary
        if is_static:
            if not isinstance(library, str):
                raise ValueError(
                    "The library name must be a string if `is_static` is " + \
                    "set to `True`."
                )
            library = PlatformStatics.get_static_lib_name(library)
        elif is_shared:
            if not isinstance(library, str):
                raise ValueError(
                    "The library name must be a string if `is_shared` is " + \
                    "set to `True`."
                )
            library = PlatformStatics.get_shared_lib_name(library)
        elif isinstance(library, Path):
            library = str(library.resolve())

        # If the library has already been added, don't generate new CMake code
        if not self._link_libraries.select_set(scope).add(library):
            return

        # Generate the CMake code
        generator = self._build_scripts.get_or_add_build_script().generator
        with generator.open_method_block("target_link_libraries") as b:
            b.add_arguments(self._target_name)
            b.add_keyword_arguments(
                scope.value,
                library
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
        full_target = self._get_full_target()
        props: Dict[str, object] = {}
        props["type"] = full_target._target_type.value
        props["sources"] = full_target._sources.to_trace_dict()
        props["include_directories"] = \
            full_target._include_directories.to_trace_dict()
        props["link_libraries"] = full_target._link_libraries.to_trace_dict()
        props["is_installed"] = full_target._is_installed
        props["install_path"] = full_target._install_path.value \
            if full_target._install_path else "<cmake_default>"

        generator.write_file({
            self.target_name: props
        }, output_path)


    def install(self,
        install_path: Optional[str] = None) -> None:
        """
        Installs the target.
        @param install_path Path to install the target to. If this is `None`,
          the path that the target will be installed to will be CMake's default
          path for the target type.
        """
        # If the target has already been configured to be installed, don't
        #   generate new CMake code
        if self._is_installed:
            return

        self._is_installed = True
        if install_path:
            self._install_path = Traced(install_path)

        # Generate the CMake code
        generator = self._build_scripts.get_or_add_build_script().generator
        with generator.open_method_block("install") as b:
            b.add_keyword_arguments(
                "TARGETS",
                self._target_name
            )
            if self._install_path:
                b.add_keyword_arguments(
                    "DESTINATION",
                    self._install_path.value
                )


    def _get_full_target(self) -> ITarget:
        """
        Gets a target instance that includes all values for the target.
        Target instances normally do not include values from targets that
          they link to. The target instance returned by this method contains
          all values for the target, including values from linked-to targets.
        @returns A target instance that includes all values from targets that
          this target links to.
        """
        # Create the target to return
        target = ITarget(
            self._build_scripts,
            self._target_name,
            self._target_type
        )

        # Populate the target with properties from each linked-to target
        linked_targets = [
            target.value
            for target in self._link_libraries.select_set(EScope.PUBLIC)
            if isinstance(target.value, ITarget)
        ]
        linked_targets.extend([
            target.value
            for target in self._link_libraries.select_set(EScope.INTERFACE)
            if isinstance(target.value, ITarget)
        ])

        # Merge all properties from linked targets into the target
        # Note that the linked target's own linked targets should not be added
        #   to the full target
        for linked_target in linked_targets:
            full_linked_target = linked_target._get_full_target()
            target._sources.merge(full_linked_target._sources)
            target._include_directories.merge(
                full_linked_target._include_directories
            )

        # Merge the properties from this target into the target
        target._sources.merge(
            self._sources,
            merge_private=True
        )
        target._include_directories.merge(
            self._include_directories,
            merge_private=True
        )
        target._link_libraries.merge(
            self._link_libraries,
            merge_private=True
        )
        target._link_libraries.merge(
            self._link_libraries,
            merge_private=True
        )
        target._is_installed = self._is_installed
        target._install_path = self._install_path

        return target
