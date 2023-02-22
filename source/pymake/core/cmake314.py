import os
from pathlib import Path
from pymake.common.cmake_version import ECMakeVersion
from pymake.core.cmake import ICMake
from pymake.core.preset import Preset
from pymake.core.pymake_args import PyMakeArgs
import subprocess
from typing import List

class CMake314(ICMake):
    """
    ICMake implementation that generates CMake v3.14-compliant code.
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
            ECMakeVersion.V3_14,
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
        # Do nothing - presets are not supported in CMake v3.14


    def _run_cmake(self, args: PyMakeArgs, presets: List[Preset]) -> int:
        """
        Runs CMake to build the project.
        @param args Arguments that were passed to PyMake.
        @param presets Presets that should be used when building the project.
          Will always contain at least one value.
        @returns The exit code of the CMake process.
        """
        # In the dev container, CMake is in the /usr/bin directory
        cmake = "cmake3.14"

        # Get the full preset values to use
        preset = presets[0].as_full_preset()
        if len(presets) > 1:
            for p in presets[1:]:
                preset.merge(p.as_full_preset())

        # Fall back to CMake defaults if values aren't provided
        binary_dir = preset.binary_dir if preset.binary_dir else "build"

        # Get the environment variables to use
        env_vars = preset.env_variables
        env_vars.update(os.environ)

        # Generate the configure command
        cmake_configure_cmd = [
            cmake,
            "-S",
            str(self._generated_dir),
            "-B",
            binary_dir
        ]
        if preset.generator:
            cmake_configure_cmd.extend([
                "-G",
                preset.generator
            ])
        if preset.install_dir:
            cmake_configure_cmd.extend([
                "-DCMAKE_INSTALL_PREFIX=" + preset.install_dir
            ])
        for k, v in preset.cache_variables.items():
            cmake_configure_cmd.extend([
                "-D" + k + "=" + v
            ])
        if args.verbose:
            cmake_configure_cmd.append("--verbose")

        # Run the configuration step
        print(f"Running command: {' '.join(cmake_configure_cmd)}")
        configure_process = subprocess.run(
            cmake_configure_cmd,
            env=env_vars,
            shell=False
        )
        if configure_process.returncode != 0:
            return configure_process.returncode

        # Generate the build command
        cmake_build_cmd = [
            cmake,
            "--build",
            binary_dir,
            "--target",
            "install"
        ]

        # Run the build step
        print(f"Running command: {' '.join(cmake_build_cmd)}")
        build_process = subprocess.run(
            cmake_build_cmd,
            env=env_vars,
            shell=False
        )
        return build_process.returncode
