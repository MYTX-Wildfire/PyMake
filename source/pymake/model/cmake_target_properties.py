from pathlib import Path
from pymake.common.cpp_standard import ECppStandard
from pymake.core.scoped_sets import ScopedSets
from pymake.model.cmake_config_target_properties import CMakeConfigTargetProperties
from typing import Dict, List, Optional, Tuple

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
        self._config_properties: Dict[str, CMakeConfigTargetProperties] = {}

        ## Command line to use for clang-tidy.
        # If this is empty, clang-tidy will not be run.
        self._clang_tidy: List[str] = []

        ## Directory that clang-tidy should output suggested changes to.
        # @invariant This will always be an absolute path.
        self._clang_tidy_export_fixes_dir: Optional[Path] = None

        ## Compiler launcher to use for the target.
        # @invariant This will always be an absolute path to a file.
        self._compiler_launcher: Optional[Path] = None

        ## Command line to use for cppcheck.
        # If this is empty, cppcheck will not be run.
        self._cpp_check: List[str] = []

        ## Command line to use for cpplint.
        # If this is empty, cpplint will not be run.
        self._cpp_lint: List[str] = []

        ## Command line to use for include-what-you-use.
        # If this is empty, include-what-you-use will not be run.
        self._iwyu: List[str] = []

        ## Linker launcher to use for the target.
        # @invariant This will always be an absolute path to a file.
        self._linker_launcher: Optional[Path] = None

        ## Visibility preset to use for the target.
        self._visibility_preset: Optional[str] = None

        ## Paths of additional files and folders to clean.
        self._additional_clean_files: List[Path] = []

        ## Path to the target's binary directory.
        # The exact binary directory that the target will use is dependent on
        #   the location of the make.py file that defines the target and the
        #   visitor implementation used to generate CMake files.
        self._binary_dir: Optional[Path] = None

        ## The C++ standard to use when compiling the target.
        # @note This is not handled by a `CMakeLanguageTargetProperties` object
        #   because it's not generic enough to be placed in that class.
        self._cxx_standard: Optional[ECppStandard] = None

        ## Whether the target should be excluded from the "all" target.
        self._exclude_from_all: bool = False

        ## Paths to add to the binary's build rpath.
        # Each path in this list may be a relative or absolute path.
        self._build_rpaths: List[Path] = []

        ## Whether the binary's build rpath should use the $ORIGIN variable.
        self._build_rpath_use_origin: bool = False

        ## Paths to add to the binary's install rpath.
        # Each path in this list may be a relative or absolute path.
        self._install_rpaths: List[Path] = []

        ## Whether the target is an imported target.
        self._imported: bool = False

        ## The name of the imported library.
        self._imported_name: Optional[str] = None

        ## The name of the imported implementation library.
        self._imported_implib_name: Optional[str] = None

        ## The path of the imported library files.
        # @invariant This will always be an absolute path.
        self._imported_location: Optional[Path] = None

        ## Whether to enable interprocedural optimization for the target.
        self._interprocedural_optimization: bool = False

        ## Base name to use for the target's output file.
        # If this is none, the name will be assigned automatically using the
        #   CMake target name.
        # @warning This should not include the file extension.
        self._output_name: Optional[str] = None

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

        ## Options to pass to the linker.
        self._link_options: ScopedSets[str] = ScopedSets()

        ## Whether to enable position independent code for the target.
        self._position_independent_code: bool = False

        ## Prefix to append to the target's base name.
        # If this is none, the prefix will be determined automatically based on
        #   the target type and current platform.
        self._prefix: Optional[str] = None

        ## Sources to add to the target.
        # @invariant Each path in this set will be an absolute path.
        self._sources: ScopedSets[Path] = ScopedSets()
