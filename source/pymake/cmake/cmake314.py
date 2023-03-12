from pymake.cmake.cmake import ICMake
from pymake.model.cmake_build_config import CMakeBuildConfig
from pymake.model.pymake_project import PyMakeProject
from pymake.model.preset import Preset
import os
import subprocess
from typing import List

class CMake314(ICMake):
    """
    Class for handling CMake 3.25 behavior.
    """
    def configure(self,
        project: PyMakeProject,
        presets: List[Preset]) -> int:
        """
        Runs the CMake configure step on the project.
        @param project The project to configure.
        @param presets The preset(s) to configure CMake to use. Must contain at
          least one element.
        @return The exit code of the CMake configure step.
        """
        assert presets

        # Get the full build configuration to be configured
        build_config = CMakeBuildConfig()
        for preset in presets:
            build_config = build_config.apply(preset.get_full_build_config())

        # Build the CMake command to invoke
        cmake_cmd = [
            "cmake3.14",
            "-S", str(project.generated_dir),
            "-B", str(project.build_dir)
        ]

        if build_config.cmake_build_type:
            cmake_cmd.append(
                f"-DCMAKE_BUILD_TYPE={build_config.cmake_build_type}"
            )

        if build_config.export_compile_commands:
            cmake_cmd.append("-DCMAKE_EXPORT_COMPILE_COMMANDS=ON")

        if build_config.generator:
            cmake_cmd.append("-G")
            cmake_cmd.append(build_config.generator)

        if build_config.generator_executable:
            cmake_cmd.append(
                f"-DCMAKE_MAKE_PROGRAM={build_config.generator_executable}"
            )

        if build_config.toolchain_file:
            cmake_cmd.append(
                f"-DCMAKE_TOOLCHAIN_FILE={build_config.toolchain_file}"
            )

        if build_config.compiler_launcher:
            cmake_cmd.append(
                f"-DCMAKE_C_COMPILER_LAUNCHER={build_config.compiler_launcher}"
            )
            cmake_cmd.append(
                f"-DCMAKE_CXX_COMPILER_LAUNCHER={build_config.compiler_launcher}"
            )

        if build_config.linker_launcher:
            cmake_cmd.append(
                f"-DCMAKE_C_LINKER_LAUNCHER={build_config.linker_launcher}"
            )
            cmake_cmd.append(
                f"-DCMAKE_CXX_LINKER_LAUNCHER={build_config.linker_launcher}"
            )

        if build_config.cxx_compiler:
            cmake_cmd.append(
                f"-DCMAKE_CXX_COMPILER={build_config.cxx_compiler}"
            )

        if build_config.install_path:
            cmake_cmd.append(
                f"-DCMAKE_INSTALL_PREFIX={build_config.install_path}"
            )

        for name, value in build_config.cmake_vars.items():
            cmake_cmd.append(f"-D{name}={value}")

        # Get the environment variables to set for the command
        env_vars = build_config.env_vars
        env_vars.update(os.environ)

        # Run the CMake command
        print("Running command: " + " ".join(cmake_cmd))
        return subprocess.run(
            cmake_cmd,
            env=env_vars,
        ).returncode


    def build(self,
        project: PyMakeProject,
        presets: List[Preset]) -> int:
        """
        Runs the CMake build step on the project.
        @param project The project to build.
        @param presets The preset(s) to build. Must contain at least one element.
        @return The exit code of the CMake build step.
        """
        assert presets

        # Get the full build configuration to be built
        build_config = CMakeBuildConfig()
        for preset in presets:
            build_config = build_config.apply(preset.get_full_build_config())

        # Build the CMake command to invoke
        cmake_cmd = [
            "cmake3.14",
            "--build", str(project.build_dir)
        ]
        if build_config.clean_build:
            cmake_cmd.append("--clean-first")

        for target in build_config.targets:
            cmake_cmd.append("--target")
            cmake_cmd.append(target)
        if not build_config.targets:
            cmake_cmd.append("--target")
            cmake_cmd.append("install")

        # Get the environment variables to set for the command
        env_vars = build_config.env_vars
        env_vars.update(os.environ)

        # Run the CMake command
        print("Running command: " + " ".join(cmake_cmd))
        return subprocess.run(
            cmake_cmd,
            env=env_vars,
        ).returncode
