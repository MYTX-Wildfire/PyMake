from pathlib import Path
from pymake.core.build_script import BuildScript
from pymake.common.sanitizer_flags import ESanitizerFlags
from pymake.common.target_type import ETargetType
from pymake.model.targets.imported.imported_target import ImportedTarget

class ExternalLibraryTarget(ImportedTarget):
    """
    Represents an external library that PyMake targets may link to.
    External libraries are represented in generated CMake code as imported
      targets.
    @todo Update this to support the other built-in CMake build configurations
       and arbitrary configurations.
    """
    def __init__(self,
        target_name: str,
        target_type: ETargetType,
        debug_path: Path,
        release_path: Path,
        sanitizer_flags: int = ESanitizerFlags.NONE):
        """
        Initializes the external library.
        @param target_name The name of the target to create for the library.
        @param target_type The type of the library. Must be either static or
          shared.
        @param debug_path Path to the debug version of the library. Must be an
          absolute path.
        @param release_path Path to the release version of the library. Must be
          an absolute path.
        @param sanitizer_flags The sanitizers that were enabled when the library
          was compiled.
        """
        super().__init__(
            target_name,
            target_type,
            sanitizer_flags
        )

        # These values are provided by PyMake code and should be valid
        assert target_type in (ETargetType.STATIC, ETargetType.SHARED), \
          "External libraries must be either static or shared."
        assert debug_path.is_absolute(), "Debug path must be absolute."
        assert release_path.is_absolute(), "Release path must be absolute."
        assert debug_path.exists(), "Debug path does not exist."
        assert debug_path.is_file(), "Debug path is not to a file."
        assert release_path.exists(), "Debug path does not exist."
        assert release_path.is_file(), "Debug path is not to a file."

        # Store values internally
        self._debug_path = debug_path
        self._release_path = release_path
        self._library_type = target_type


    def generate_target(self,
        build_script: BuildScript) -> None:
        """
        Generates the CMake code for the target.
        @param build_script Build script to write the target to.
        """
        generator = build_script.generator
        with generator.open_method_block("add_library") as b:
            b.add_arguments(
                self._target_name,
                self._target_type.name,
                "IMPORTED"
            )
        with generator.open_method_block("set_target_properties") as b:
            b.add_arguments(
                self._target_name,
                "PROPERTIES"
            )
            b.add_keyword_arguments(
                "IMPORTED_LOCATION_DEBUG",
                str(self._debug_path)
            )
            b.add_keyword_arguments(
                "IMPORTED_LOCATION_RELEASE",
                str(self._release_path)
            )
            b.add_keyword_arguments(
                "IMPORTED_CONFIGURATIONS",
                "DEBUG;RELEASE"
            )
