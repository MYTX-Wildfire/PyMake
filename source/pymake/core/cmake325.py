import json
from pathlib import Path
from pymake.common.cmake_version import ECMakeVersion
from pymake.core.cmake import ICMake
from pymake.core.preset import Preset
from pymake.core.pymake_args import PyMakeArgs
from typing import Dict, List

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
            b.add_keyword_arguments("VERSION", self._minimum_version.value)


    def _generate_presets(self, output_path: Path) -> None:
        """
        Generates the CMakePresets.json file (if supported).
        @param output_path Path where the CMakePresets.json file should be
          written.
        """
        # Generate the dictionary to convert to a JSON object
        presets_file: Dict[str, object] = {}
        presets_file["version"] = 6
        presets_file["cmakeMinimumRequired"] = {
            "major": 3,
            "minor": 25,
            "patch": 0
        }

        # Add the presets as configure presets
        configure_presets: List[Dict[str, object]] = []
        for preset in self._presets.values():
            configure_presets.append(preset.as_configure_preset())
        presets_file["configurePresets"] = configure_presets

        # Add the presets as build presets
        build_presets: List[Dict[str, object]] = []
        for preset in self._presets.values():
            build_presets.append(preset.as_build_preset())
        presets_file["buildPresets"] = build_presets

        # Write the presets file
        with open(output_path, "w") as f:
            json.dump(presets_file, f, indent=2)


    def _run_cmake(self, args: PyMakeArgs, presets: List[Preset]) -> int:
        """
        Runs CMake to build the project.
        @param args Arguments that were passed to PyMake.
        @param presets Presets that should be used when building the project.
          Will always contain at least one value.
        @returns The exit code of the CMake process.
        """
        # In the dev container, CMake is in the /usr/bin directory
        cmake = "cmake3.25"
