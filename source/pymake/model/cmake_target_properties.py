from pathlib import Path
from pymake.common.cxx_standard import ECxxStandard
from pymake.core.scoped_sets import ScopedSets
from pymake.model.cmake_config_target_properties import CMakeConfigTargetProperties
from pymake.tracing.caller_info import CallerInfo
from pymake.tracing.traced import Traced
from pymake.tracing.traced_dict import TracedDict
from typing import Iterable, List, Optional, Set, Tuple

class CMakeTargetProperties:
    """
    Stores properties that may be set on a CMake target.
    @warning This class defines properties for all CMake target properties
      regardless of whether they're relevant to a particular target type.
      Classes for a specific target type should only expose the properties
      that are relevant to that target type.
    """
    def __init__(self):
        """
        Initializes the properties with default values.
        """
        ## Config-specific properties.
        # Each entry in this dictionary is indexed by the name of the build
        #   configuration the values are for. Build configuration names are not
        #   required to match the built-in CMake build configurations' names.
        self._config_properties: TracedDict[str, CMakeConfigTargetProperties] = \
            TracedDict()

        ## Command line to use for clang-tidy.
        # If this is empty, clang-tidy will not be run.
        self._clang_tidy: Traced[List[str]] = Traced([])

        ## Directory that clang-tidy should output suggested changes to.
        # @invariant This will always be an absolute path.
        self._clang_tidy_export_fixes_dir: Traced[Optional[Path]] = Traced(None)

        ## Compiler launcher to use for the target.
        # @invariant This will always be an absolute path to a file.
        self._compiler_launcher: Traced[Optional[Path]] = Traced(None)

        ## Command line to use for cppcheck.
        # If this is empty, cppcheck will not be run.
        self._cpp_check: Traced[List[str]] = Traced([])

        ## Command line to use for cpplint.
        # If this is empty, cpplint will not be run.
        self._cpp_lint: Traced[List[str]] = Traced([])

        ## Command line to use for include-what-you-use.
        # If this is empty, include-what-you-use will not be run.
        self._iwyu: Traced[List[str]] = Traced([])

        ## Linker launcher to use for the target.
        # @invariant This will always be an absolute path to a file.
        self._linker_launcher: Traced[Optional[Path]] = Traced(None)

        ## Visibility preset to use for the target.
        self._visibility_preset: Traced[Optional[str]] = Traced(None)

        ## Paths of additional files and folders to clean.
        self._additional_clean_files: List[Traced[Path]] = []

        ## The C++ standard to use when compiling the target.
        # @note This is not handled by a `CMakeLanguageTargetProperties` object
        #   because it's not generic enough to be placed in that class.
        self._cxx_standard: Traced[Optional[ECxxStandard]] = Traced(None)

        ## Whether the target should be excluded from the "all" target.
        self._exclude_from_all = Traced(False)

        ## Paths to add to the binary's build rpath.
        # Each path in this list may be a relative or absolute path.
        self._build_rpaths: List[Traced[Path]] = []

        ## Whether the binary's build rpath should use the $ORIGIN variable.
        self._build_rpath_use_origin = Traced(False)

        ## Whether the target should be installed.
        self._should_install = Traced(True)

        ## The path to install the target to.
        # @invariant This may be an absolute or relative path. Relative paths
        #   will be resolved relative to the project's install prefix.
        self._install_path: Traced[Optional[Path]] = Traced(None)

        ## Paths to add to the binary's install rpath.
        # Each path in this list may be a relative or absolute path.
        self._install_rpaths: List[Traced[Path]] = []

        ## Whether the binary's install rpath should use the link paths.
        self._install_rpath_use_link_path = Traced(False)

        ## Whether the target is an imported target.
        self._imported = Traced(False)

        ## The name of the imported library.
        self._imported_name: Traced[Optional[str]] = Traced(None)

        ## The name of the imported implementation library.
        self._imported_implib_name: Traced[Optional[str]] = Traced(None)

        ## The path of the imported library files.
        # @invariant This will always be an absolute path.
        self._imported_location: Traced[Optional[Path]] = Traced(None)

        ## Whether to enable interprocedural optimization for the target.
        self._interprocedural_optimization = Traced(False)

        ## Base name to use for the target's output file.
        # If this is none, the name will be assigned automatically using the
        #   CMake target name.
        # @warning This should not include the file extension.
        self._output_name: Traced[Optional[str]] = Traced(None)

        ## Compile definitions to add to the target.
        # Each definition is a tuple of the form (name, value). If the value is
        #   None, the definition will be added as a preprocessor definition with
        #   no value.
        self._compile_definitions: ScopedSets[Tuple[str, Optional[str]]] = \
            ScopedSets()

        ## Compile options to add to the target.
        self._compile_options: ScopedSets[str] = ScopedSets()

        ## Include directories to add to the target.
        # @invariant Each path in this set will be an absolute path.
        self._include_directories: ScopedSets[Path] = ScopedSets()

        ## Directories to add to the linker's search path.
        # @invariant Each path in this set will be an absolute path.
        self._link_directories: ScopedSets[Path] = ScopedSets()

        ## Names of libraries or targets to link to.
        self._link_libraries: ScopedSets[str] = ScopedSets()

        ## Options to pass to the linker.
        self._link_options: ScopedSets[str] = ScopedSets()

        ## Whether to enable position independent code for the target.
        self._position_independent_code = Traced(False)

        ## Prefix to append to the target's base name.
        # If this is none, the prefix will be determined automatically based on
        #   the target type and current platform.
        self._prefix: Traced[Optional[str]] = Traced(None)

        ## Sources to add to the target.
        # @invariant Each path in this set will be an absolute path.
        self._sources: ScopedSets[Path] = ScopedSets()


    @property
    def configs(self) -> Set[str]:
        """
        Gets the configuration options to use for the target.
        """
        return { c for c, _ in self._config_properties }


    @property
    def clang_tidy(self) -> Traced[List[str]]:
        """
        Gets the command line to use for clang-tidy.
        """
        return self._clang_tidy


    @clang_tidy.setter
    def clang_tidy(self, value: List[str]) -> None:
        """
        Sets the command line to use for clang-tidy.
        """
        self._clang_tidy = Traced(value)


    @property
    def clang_tidy_export_fixes_dir(self) -> Traced[Optional[Path]]:
        """
        Gets the directory that clang-tidy should output suggested changes to.
        """
        return self._clang_tidy_export_fixes_dir


    @clang_tidy_export_fixes_dir.setter
    def clang_tidy_export_fixes_dir(self, value: Optional[Path]) -> None:
        """
        Sets the directory that clang-tidy should output suggested changes to.
        """
        self._clang_tidy_export_fixes_dir = Traced(value)


    @property
    def compiler_launcher(self) -> Traced[Optional[Path]]:
        """
        Gets the compiler launcher to use for the target.
        """
        return self._compiler_launcher


    @compiler_launcher.setter
    def compiler_launcher(self, value: Optional[Path]) -> None:
        """
        Sets the compiler launcher to use for the target.
        """
        self._compiler_launcher = Traced(value)


    @property
    def cpp_check(self) -> Traced[List[str]]:
        """
        Gets the command line to use for cppcheck.
        """
        return self._cpp_check


    @cpp_check.setter
    def cpp_check(self, value: List[str]) -> None:
        """
        Sets the command line to use for cppcheck.
        """
        self._cpp_check = Traced(value)


    @property
    def cpp_lint(self) -> Traced[List[str]]:
        """
        Gets the command line to use for cpplint.
        """
        return self._cpp_lint


    @cpp_lint.setter
    def cpp_lint(self, value: List[str]) -> None:
        """
        Sets the command line to use for cpplint.
        """
        self._cpp_lint = Traced(value)


    @property
    def iwyu(self) -> Traced[List[str]]:
        """
        Gets the command line to use for include-what-you-use.
        """
        return self._iwyu


    @iwyu.setter
    def iwyu(self, value: List[str]) -> None:
        """
        Sets the command line to use for include-what-you-use.
        """
        self._iwyu = Traced(value)


    @property
    def linker_launcher(self) -> Traced[Optional[Path]]:
        """
        Gets the linker launcher to use for the target.
        """
        return self._linker_launcher


    @linker_launcher.setter
    def linker_launcher(self, value: Optional[Path]) -> None:
        """
        Sets the linker launcher to use for the target.
        """
        self._linker_launcher = Traced(value)


    @property
    def visibility_preset(self) -> Traced[Optional[str]]:
        """
        Gets the visibility preset to use for the target.
        """
        return self._visibility_preset


    @visibility_preset.setter
    def visibility_preset(self, value: Optional[str]) -> None:
        """
        Sets the visibility preset to use for the target.
        """
        self._visibility_preset = Traced(value)


    @property
    def additional_clean_files(self) -> List[Traced[Path]]:
        """
        Gets the additional files to clean when cleaning the target.
        """
        return self._additional_clean_files


    @property
    def cxx_standard(self) -> Traced[Optional[ECxxStandard]]:
        """
        Gets the C++ standard to use for the target.
        """
        return self._cxx_standard


    @cxx_standard.setter
    def cxx_standard(self, value: Optional[ECxxStandard]) -> None:
        """
        Sets the C++ standard to use for the target.
        """
        self._cxx_standard = Traced(value)


    @property
    def exclude_from_all(self) -> Traced[bool]:
        """
        Gets whether the target should be excluded from the default build.
        """
        return self._exclude_from_all


    @exclude_from_all.setter
    def exclude_from_all(self, value: bool) -> None:
        """
        Sets whether the target should be excluded from the default build.
        """
        self._exclude_from_all = Traced(value)


    @property
    def build_rpaths(self) -> List[Traced[Path]]:
        """
        Gets the build rpaths to use for the target.
        """
        return self._build_rpaths


    @property
    def should_install(self) -> Traced[bool]:
        """
        Gets whether the target should be installed.
        """
        return self._should_install


    @property
    def install_path(self) -> Traced[Optional[Path]]:
        """
        Gets the install path to use for the target.
        """
        return self._install_path


    @property
    def build_rpath_use_origin(self) -> Traced[bool]:
        """
        Gets whether the build rpaths should use the origin flag.
        """
        return self._build_rpath_use_origin


    @property
    def install_rpaths(self) -> List[Traced[Path]]:
        """
        Gets the install rpaths to use for the target.
        """
        return self._install_rpaths


    @property
    def install_rpath_use_link_path(self) -> Traced[bool]:
        """
        Gets whether the install rpaths should use the link paths.
        """
        return self._install_rpath_use_link_path


    @property
    def imported(self) -> Traced[bool]:
        """
        Gets whether the target is imported.
        """
        return self._imported


    @imported.setter
    def imported(self, value: bool) -> None:
        """
        Sets whether the target is imported.
        """
        self._imported = Traced(value)


    @property
    def imported_name(self) -> Traced[Optional[str]]:
        """
        Gets the name of the imported target.
        """
        return self._imported_name


    @imported_name.setter
    def imported_name(self, value: Optional[str]) -> None:
        """
        Sets the name of the imported target.
        """
        self._imported_name = Traced(value)


    @property
    def imported_implib_name(self) -> Traced[Optional[str]]:
        """
        Gets the implementation library name of the imported target.
        """
        return self._imported_implib_name


    @imported_implib_name.setter
    def imported_implib_name(self, value: Optional[str]) -> None:
        """
        Sets the implementation library name of the imported target.
        """
        self._imported_implib_name = Traced(value)


    @property
    def imported_location(self) -> Traced[Optional[Path]]:
        """
        Gets the location of the imported target.
        """
        return self._imported_location


    @imported_location.setter
    def imported_location(self, value: Optional[Path]) -> None:
        """
        Sets the location of the imported target.
        """
        self._imported_location = Traced(value)


    @property
    def interprocedural_optimization(self) -> Traced[bool]:
        """
        Gets whether interprocedural optimization is enabled for the target.
        """
        return self._interprocedural_optimization


    @interprocedural_optimization.setter
    def interprocedural_optimization(self, value: bool) -> None:
        """
        Sets whether interprocedural optimization is enabled for the target.
        """
        self._interprocedural_optimization = Traced(value)


    @property
    def output_name(self) -> Traced[Optional[str]]:
        """
        Gets the output name of the target.
        """
        return self._output_name


    @output_name.setter
    def output_name(self, value: Optional[str]) -> None:
        """
        Sets the output name of the target.
        """
        self._output_name = Traced(value)


    @property
    def compile_definitions(self) -> ScopedSets[Tuple[str, Optional[str]]]:
        """
        Gets the compile definitions to use for the target.
        """
        return self._compile_definitions


    @property
    def compile_options(self) -> ScopedSets[str]:
        """
        Gets the compile options to use for the target.
        """
        return self._compile_options


    @property
    def include_directories(self) -> ScopedSets[Path]:
        """
        Gets the include directories to use for the target.
        """
        return self._include_directories


    @property
    def link_directories(self) -> ScopedSets[Path]:
        """
        Gets the link directories to use for the target.
        """
        return self._link_directories


    @property
    def link_libraries(self) -> ScopedSets[str]:
        """
        Gets the link libraries to use for the target.
        """
        return self._link_libraries


    @property
    def link_options(self) -> ScopedSets[str]:
        """
        Gets the link options to use for the target.
        """
        return self._link_options


    @property
    def position_independent_code(self) -> Traced[bool]:
        """
        Gets whether position-independent code is enabled for the target.
        """
        return self._position_independent_code


    @position_independent_code.setter
    def position_independent_code(self, value: bool) -> None:
        """
        Sets whether position-independent code is enabled for the target.
        """
        self._position_independent_code = Traced(value)


    @property
    def prefix(self) -> Traced[Optional[str]]:
        """
        Gets the prefix to use for the target.
        """
        return self._prefix


    @prefix.setter
    def prefix(self, value: Optional[str]) -> None:
        """
        Sets the prefix to use for the target.
        """
        self._prefix = Traced(value)


    @property
    def sources(self) -> ScopedSets[Path]:
        """
        Gets the sources to use for the target.
        """
        return self._sources


    def add_additional_clean_files(self,
        files: str | Path | Iterable[str | Path]) -> None:
        """
        Adds additional files to clean when cleaning the target.
        @param files The files to add. Paths may be relative or absolute.
          Relative paths will be interpreted relative to the caller's directory.
        """
        if isinstance(files, (str, Path)):
            files = [files]

        # Get the path to resolve relative paths against.
        caller_info = CallerInfo.closest_external_frame()
        caller_dir = caller_info.file_path.parent

        # Add each file to the list.
        for file in files:
            if isinstance(file, str):
                file = Path(file)
            if not file.is_absolute():
                file = caller_dir / file
            file = file.resolve()

            self._additional_clean_files.append(file)


    def add_build_rpath(self, rpath: str | Path) -> None:
        """
        Adds an rpath to use when building the target.
        @param rpath The rpath to add. Paths may be relative or absolute.
          Relative paths will not be converted to absolute paths.
        """
        if isinstance(rpath, str):
            rpath = Path(rpath)
        self._build_rpaths.append(Traced(rpath))


    def add_install_rpath(self, rpath: str | Path) -> None:
        """
        Adds an rpath to use when installing the target.
        @param rpath The rpath to add. Paths may be relative or absolute.
          Relative paths will not be converted to absolute paths.
        """
        if isinstance(rpath, str):
            rpath = Path(rpath)
        self._install_rpaths.append(Traced(rpath))


    def get_config_properties(self, config: str) -> CMakeConfigTargetProperties:
        """
        Gets the config-specific properties for the given build configuration.
        @param config The name of the build configuration to get properties for.
        @return The config-specific properties for the given build configuration.
        """
        return self._config_properties[config]


    def install(self, install_dir: str | Path | None) -> None:
        """
        Installs the target.
        @param install_dir The directory to install the target to. If this is a
          relative path, it will be interpreted relative to the install prefix.
          If this is none, CMake's default install directory for the target type
          will be used.
        """
        if isinstance(install_dir, str):
            install_dir = Path(install_dir)

        self._should_install = Traced(True)
        self._install_dir = Traced(install_dir)
