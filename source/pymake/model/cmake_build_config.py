from __future__ import annotations
from pathlib import Path
from pymake.common.cmake_build_type import ECMakeBuildType
from pymake.common.cmake_generator import ECMakeGenerator
from pymake.tracing.caller_info import CallerInfo
from pymake.util.path_statics import PathStatics
from typing import Any, Callable, List, Optional

class CMakeBuildConfig:
    """
    Stores all properties that may be set for a CMake build configuration.
    This class is used internally within presets to store the preset's values.
      Since multiple presets may be used, this class also supports applying a
      build configuration "on top of" another build configuration, which
      overwrites the base build configuration's values with the values from the
      applied build configuration. Any value that is not set in the applied
      build configuration will use the value from the base build configuration.
    Build configurations are meant for internal use only and represent values
      to be passed to CMake. Since they are not meant for direct use by users
      and each build configuration may be generated from one or more presets,
      build configurations do not have names.
    """
    ## List of getters for all properties in the config.
    # @invariant This list is maintained in the same order as the setters
    #   list.
    _getters: List[Callable[[CMakeBuildConfig], Optional[Any]]] = [
        lambda x: x._cmake_build_type,
        lambda x: x._export_compile_commands,
        lambda x: x._generator,
        lambda x: x._generator_executable,
        lambda x: x._toolchain_file,
        lambda x: x._compiler_launcher,
        lambda x: x._linker_launcher,
        lambda x: x._cxx_compiler,
        lambda x: x._install_path
    ]

    ## List of setters for all properties in the config.
    # @invariant This list is maintained in the same order as the getters
    #   list.
    _setters: List[Callable[[CMakeBuildConfig, Optional[Any]], None]] = [
        lambda x, value: setattr(x, "_cmake_build_type", value),
        lambda x, value: setattr(x, "_export_compile_commands", value),
        lambda x, value: setattr(x, "_generator", value),
        lambda x, value: setattr(x, "_generator_executable", value),
        lambda x, value: setattr(x, "_toolchain_file", value),
        lambda x, value: setattr(x, "_compiler_launcher", value),
        lambda x, value: setattr(x, "_linker_launcher", value),
        lambda x, value: setattr(x, "_cxx_compiler", value),
        lambda x, value: setattr(x, "_install_path", value)
    ]

    def __init__(self):
        """
        Initializes the object with default values for all properties.
        """
        ## CMake build type that the config maps to.
        self._cmake_build_type: Optional[str] = None

        ## Whether to export compile commands.
        self._export_compile_commands: Optional[bool] = None

        ## Generator to use for CMake.
        self._generator: Optional[str] = None

        ## Path to the generator executable.
        # @invariant This will always be an absolute path.
        self._generator_executable: Optional[Path] = None

        ## Toolchain file to use for CMake.
        self._toolchain_file: Optional[Path] = None

        ## Compiler launcher to use for CMake.
        # @invariant This will always be an absolute path.
        self._compiler_launcher: Optional[Path] = None

        ## Linker launcher to use for CMake.
        # @invariant This will always be an absolute path.
        self._linker_launcher: Optional[Path] = None

        ## C++ compiler to use for CMake.
        # @invariant This will always be an absolute path.
        self._cxx_compiler: Optional[Path] = None

        ## Path to install to.
        # @invariant This will always be an absolute path.
        self._install_path: Optional[Path] = None


    def apply(self,
        other: CMakeBuildConfig) -> CMakeBuildConfig:
        """
        Applies the values from another build configuration to this one.
        Values from the other build configuration will overwrite the values in
          this build configuration.
        @param other The build configuration to apply.
        @return A new build configuration containing the result of applying the
          other build configuration to this one.
        """
        config = CMakeBuildConfig()

        # Prioritize values from the other build configuration over values from
        #   this one
        for getter, setter in zip(
            CMakeBuildConfig._getters, CMakeBuildConfig._setters):
            value = getter(other)
            if value:
                setter(config, value)
            else:
                setter(config, getter(self))

        return config


    @property
    def cmake_build_type(self) -> Optional[str]:
        """
        Gets the CMake build type that the config maps to.
        """
        return self._cmake_build_type


    @cmake_build_type.setter
    def cmake_build_type(self,
        value: Optional[str | ECMakeBuildType]) -> None:
        """
        Sets the CMake build type that the config maps to.
        """
        if isinstance(value, ECMakeBuildType):
            value = value.value
        else:
            self._cmake_build_type = value


    @property
    def export_compile_commands(self) -> Optional[bool]:
        """
        Gets whether to export compile commands.
        """
        return self._export_compile_commands


    @export_compile_commands.setter
    def export_compile_commands(self,
        value: Optional[bool]) -> None:
        """
        Sets whether to export compile commands.
        """
        self._export_compile_commands = value


    @property
    def generator(self) -> Optional[str]:
        """
        Gets the generator to use for CMake.
        """
        return self._generator


    @generator.setter
    def generator(self,
        value: Optional[str | ECMakeGenerator]) -> None:
        """
        Sets the generator to use for CMake.
        """
        if isinstance(value, ECMakeGenerator):
            value = value.value
        else:
            self._generator = value


    @property
    def generator_executable(self) -> Optional[Path]:
        """
        Gets the path to the generator executable.
        """
        return self._generator_executable


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
        if value:
            self._generator_executable = self._validate_file(
                value,
                resolve_strings_using_path=True
            )
        else:
            self._generator_executable = None


    @property
    def toolchain_file(self) -> Optional[Path]:
        """
        Gets the toolchain file to use for CMake.
        """
        return self._toolchain_file


    @toolchain_file.setter
    def toolchain_file(self,
        value: Optional[str | Path]) -> None:
        """
        Sets the toolchain file to use for CMake.
        If the path is not an absolute path, the path will be resolved relative
          to the caller's directory.
        @throws ValueError Thrown if the path does not exist or is not to a file.
        """
        if value:
            self._toolchain_file = self._validate_file(
                value,
                # Toolchain files are not expected to be on the PATH, so the
                #   value should always be treated as a regular file path
                resolve_strings_using_path=False
            )
        else:
            self._toolchain_file = None


    @property
    def compiler_launcher(self) -> Optional[Path]:
        """
        Gets the compiler launcher to use for CMake.
        """
        return self._compiler_launcher


    @compiler_launcher.setter
    def compiler_launcher(self,
        value: Optional[str | Path]) -> None:
        """
        Sets the compiler launcher to use for CMake.
        @param value The compiler launcher to use for CMake. If this is a
          string, it will be resolved using the system PATH. If this is a path
          and not an absolute path, it will be resolved relative to the caller's
          directory.
        @throws ValueError Thrown if the path does not exist or is not to a file.
        @throws FileNotFoundError Thrown if the path is a string and could not
          be resolved using the system PATH.
        """
        if value:
            self._compiler_launcher = self._validate_file(
                value,
                resolve_strings_using_path=True
            )
        else:
            self._compiler_launcher = None


    @property
    def linker_launcher(self) -> Optional[Path]:
        """
        Gets the linker launcher to use for CMake.
        """
        return self._linker_launcher


    @linker_launcher.setter
    def linker_launcher(self,
        value: Optional[Path]) -> None:
        """
        Sets the linker launcher to use for CMake.
        @param value The linker launcher to use for CMake. If this is a string,
          it will be resolved using the system PATH. If this is a path and not
          an absolute path, it will be resolved relative to the caller's
          directory.
        @throws ValueError Thrown if the path does not exist or is not to a file.
        @throws FileNotFoundError Thrown if the path is a string and could not
          be resolved using the system PATH.
        """
        if value:
            self._linker_launcher = self._validate_file(
                value,
                resolve_strings_using_path=True
            )
        else:
            self._linker_launcher = None


    @property
    def cxx_compiler(self) -> Optional[Path]:
        """
        Gets the C++ compiler to use for CMake.
        """
        return self._cxx_compiler


    @cxx_compiler.setter
    def cxx_compiler(self,
        value: Optional[Path]) -> None:
        """
        Sets the C++ compiler to use for CMake.
        @param value The C++ compiler to use for CMake. If this is a string, it
          will be resolved using the system PATH. If this is a path and not an
          absolute path, it will be resolved relative to the caller's directory.
        @throws ValueError Thrown if the path does not exist or is not to a file.
        @throws FileNotFoundError Thrown if the path is a string and could not
          be resolved using the system PATH.
        """
        if value:
            self._cxx_compiler = self._validate_file(
                value,
                resolve_strings_using_path=True
            )
        else:
            self._cxx_compiler = None


    @property
    def install_path(self) -> Optional[Path]:
        """
        Gets the path to install to.
        """
        return self._install_path


    @install_path.setter
    def install_path(self,
        value: Optional[str | Path]) -> None:
        """
        Sets the path to install to.
        @param value The path to install to. If this is a relative path, it will
          be resolved relative to the caller's directory.
        """
        if not value:
            self._install_path = None
            return
        if isinstance(value, str):
            value = Path(value)

        # Get the directory to resolve relative paths against.
        caller_info = CallerInfo.closest_external_frame()
        caller_dir = caller_info.file_path.parent

        # Resolve the path.
        if not value.is_absolute():
            value = caller_dir / value
        value = value.resolve()
        self._install_path = value


    def __eq__(self, other: Any) -> bool:
        """
        Checks if this object is equal to another object.
        @param other The other object.
        @return True if the objects are equal, False otherwise.
        """
        if not isinstance(other, CMakeBuildConfig):
            return False

        for getter in CMakeBuildConfig._getters:
            if getter(self) != getter(other):
                return False
        return True


    def __ne__(self, other: Any) -> bool:
        """
        Checks if this object is not equal to another object.
        @param other The other object.
        @return True if the objects are not equal, False otherwise.
        """
        return not self == other


    def __hash__(self) -> int:
        """
        Gets the hash of this object.
        @return The hash of this object.
        """
        return hash(tuple(getter(self) for getter in CMakeBuildConfig._getters))


    def __str__(self) -> str:
        """
        Gets a string representation of this object.
        @return A string representation of this object.
        """
        return f"CMakeBuildConfig(cmake_build_type={self.cmake_build_type}, " \
            f"export_compile_commands={self.export_compile_commands}, " \
            f"generator={self.generator}, " \
            f"generator_executable={self.generator_executable}, " \
            f"toolchain_file={self.toolchain_file}, " \
            f"compiler_launcher={self.compiler_launcher}, " \
            f"linker_launcher={self.linker_launcher}, " \
            f"cxx_compiler={self.cxx_compiler}, " \
            f"install_path={self.install_path})"


    def _validate_file(self,
        file_path: str | Path,
        resolve_strings_using_path: bool) -> Path:
        """
        Validates that the given path exists and is a file.
        @param file_path The path to validate. This may be an absolute or
          relative path. If the path is relative, it will be resolved relative
          to the caller's directory. If this is a string, it will be interpreted
          as a path if `resolve_strings_using_path` is True, otherwise it will
          be interpreted as a file name that must be resolved using the system
          PATH.
        @throws ValueError Thrown if the path does not exist or is not to a file.
        @throws FileNotFoundError Thrown if the path is a string and cannot be
          resolved using the system PATH.
        @returns The resolved absolute path.
        """
        # Get the directory to resolve relative paths against.
        caller_info = CallerInfo.closest_external_frame()
        caller_dir = caller_info.file_path.parent

        return PathStatics.validate_file(
            file_path,
            caller_dir,
            resolve_strings_using_path
        )
