from pathlib import Path
from pymake.common.cmake_build_type import ECMakeBuildType
from pymake.common.cmake_generator import ECMakeGenerator
from pymake.model.cmake_build_config import CMakeBuildConfig
from typing import Optional

class Preset:
    """
    Represents a set of build parameters that can be applied to a project.
    """
    def __init__(self,
        preset_name: str):
        """
        Initializes the preset with default values.
        @param preset_name The name of the preset.
        """
        self._preset_name = preset_name

        ## Build configuration that the preset maps to.
        self._build_config = CMakeBuildConfig()


    @property
    def preset_name(self) -> str:
        """
        Gets the name of the preset.
        """
        return self._preset_name


    @property
    def cmake_build_type(self) -> Optional[str]:
        """
        Gets the CMake build type for the preset.
        """
        return self._build_config.cmake_build_type


    @cmake_build_type.setter
    def cmake_build_type(self,
        value: Optional[str | ECMakeBuildType]) -> None:
        """
        Sets the CMake build type for the preset.
        """
        self._build_config.cmake_build_type = value


    @property
    def export_compile_commands(self) -> Optional[bool]:
        """
        Gets whether to export compile commands for the preset.
        """
        return self._build_config.export_compile_commands


    @export_compile_commands.setter
    def export_compile_commands(self,
        value: Optional[bool]) -> None:
        """
        Sets whether to export compile commands for the preset.
        """
        self._build_config.export_compile_commands = value


    @property
    def generator(self) -> Optional[str]:
        """
        Gets the CMake generator for the preset.
        """
        return self._build_config.generator


    @generator.setter
    def generator(self,
        value: Optional[str | ECMakeGenerator]) -> None:
        """
        Sets the CMake generator for the preset.
        """
        self._build_config.generator = value


    @property
    def generator_executable(self) -> Optional[Path]:
        """
        Gets the CMake generator executable for the preset.
        """
        return self._build_config.generator_executable


    @generator_executable.setter
    def generator_executable(self,
        value: Optional[str | Path]) -> None:
        """
        Sets the path to the generator executable.
        @param value The generator executable to use with CMake. If this is a
          string, it will be resolved using the system PATH. If this is a path
          and not an absolute path, it will be resolved relative to the caller's
          directory.
        @throws ValueError Thrown if the path does not exist or is not to a file.
        @throws FileNotFoundError Thrown if the path is a string and could not
          be resolved using the system PATH.
        """
        self._build_config.generator_executable = value


    @property
    def toolchain_file(self) -> Optional[Path]:
        """
        Gets the toolchain file for the preset.
        """
        return self._build_config.toolchain_file


    @toolchain_file.setter
    def toolchain_file(self,
        value: Optional[str | Path]) -> None:
        """
        Sets the toolchain file to use for CMake.
        If the path is not an absolute path, the path will be resolved relative
          to the caller's directory.
        @throws ValueError Thrown if the path does not exist or is not to a file.
        """
        self._build_config.toolchain_file = value


    @property
    def compiler_launcher(self) -> Optional[Path]:
        """
        Gets the compiler launcher for the preset.
        """
        return self._build_config.compiler_launcher


    @compiler_launcher.setter
    def compiler_launcher(self,
        value: Optional[str | Path]) -> None:
        """
        Sets the compiler launcher to use for the preset.
        @param value The compiler launcher to use. If this is a string, it will
          be resolved using the system PATH. If this is a path and not an
          absolute path, it will be resolved relative to the caller's directory.
        @throws ValueError Thrown if the path does not exist or is not to a file.
        @throws FileNotFoundError Thrown if the path is a string and could not
          be resolved using the system PATH.
        """
        self._build_config.compiler_launcher = value


    @property
    def linker_launcher(self) -> Optional[Path]:
        """
        Gets the linker launcher for the preset.
        """
        return self._build_config.linker_launcher


    @linker_launcher.setter
    def linker_launcher(self,
        value: Optional[Path]) -> None:
        """
        Sets the linker launcher to use for the preset.
        @param value The linker launcher to use. If this is a string, it will be
          resolved using the system PATH. If this is a path and not an absolute
          path, it will be resolved relative to the caller's directory.
        @throws ValueError Thrown if the path does not exist or is not to a file.
        @throws FileNotFoundError Thrown if the path is a string and could not
          be resolved using the system PATH.
        """
        self._build_config.linker_launcher = value


    @property
    def cxx_compiler(self) -> Optional[Path]:
        """
        Gets the C++ compiler for the preset.
        """
        return self._build_config.cxx_compiler


    @cxx_compiler.setter
    def cxx_compiler(self,
        value: Optional[Path]) -> None:
        """
        Sets the C++ compiler to use for the preset.
        @param value The C++ compiler to use. If this is a string, it will be
          resolved using the system PATH. If this is a path and not an absolute
          path, it will be resolved relative to the caller's directory.
        @throws ValueError Thrown if the path does not exist or is not to a file.
        @throws FileNotFoundError Thrown if the path is a string and could not
          be resolved using the system PATH.
        """
        self._build_config.cxx_compiler = value


    @property
    def install_path(self) -> Optional[Path]:
        """
        Gets the install path for the preset.
        """
        return self._build_config.install_path


    @install_path.setter
    def install_path(self,
        value: Optional[str | Path]) -> None:
        """
        Sets the install path for the preset.
        @param value The path to install to. If this is a relative path, it will
          be resolved relative to the caller's directory.
        """
        self._build_config.install_path = value
