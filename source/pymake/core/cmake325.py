from pathlib import Path
from pymake.common.cmake_version import ECMakeVersion
from pymake.core.cmake import ICMake

class CMake325(ICMake):
    """
    ICMake implementation that generates CMake v3.25-compliant code.
    """
    def __init__(self,
        source_directory: str | Path = ".",
        generated_directory: str | Path = ".pymake"):
        """
        Initializes the CMake instance.
        @param source_directory Path to the directory containing the source
          files for the PyMake project. If this is a relative path, it will be
          interpreted relative to the caller's directory.
        @param generated_directory Path to the directory where PyMake should
          generate the CMake files. If this is a relative path, it will be
          interpreted relative to the caller's directory.
        """
        super().__init__(
            ECMakeVersion.V3_25,
            source_directory,
            generated_directory
        )

        # Generate the initial CMake code
        generator = self._build_scripts.get_or_add_build_script().generator
        with generator.open_method_block("cmake_minimum_required") as b:
            b.add_keyword_arguments("VERSION", str(self._minimum_version))
