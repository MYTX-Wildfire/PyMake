from __future__ import annotations
from pathlib import Path
from pymake.common.cmake_build_type import ECMakeBuildType
from pymake.common.cmake_generator import ECMakeGenerator
from pymake.generators.trace_file_generator import ITraceFileGenerator
from pymake.tracing.traced import ITraced
from typing import Dict, Iterable, Optional

class Preset(ITraced):
    """
    Represents a CMake preset.
    """
    # Name of the CMake variable used to store the build type
    CMAKE_BUILD_TYPE_VAR = "CMAKE_BUILD_TYPE"

    def __init__(self,
        name: str,
        desc: Optional[str] = None,
        is_hidden: bool = False,
        cmake_generator: Optional[str] = None,
        binary_path: Optional[str] = None,
        install_path: Optional[str] = None,
        cache_vars: Optional[Dict[str, str]] = None,
        env_vars: Optional[Dict[str, str]] = None,
        inherits: Optional[Preset] | Iterable[Preset] = None,
        is_full_preset: bool = False):
        """
        Initializes the preset.
        @param name Name of the preset.
        @param desc Description of the preset.
        @param is_hidden Whether the preset should be hidden. Hidden presets are
          not selectable when invoking PyMake.
        @param cmake_generator Name of the CMake generator.
        @param binary_path Path to the directory where CMake will generate the
          build files. If this is a relative path, it will be interpreted
          relative to the PyMake project's source directory.
        @param install_path Path to the directory where CMake will install built
          targets. If this is a relative path, it will be interpreted relative
          to the PyMake project's source directory.
        @param cache_vars Dictionary of cache variables to set.
        @param env_vars Dictionary of environment variables to set.
        @param inherits Presets that this preset inherits from.
        @param is_full_preset Whether the preset includes all values from
          presets that it inherits from.
        """
        super().__init__()

        self._name = name
        self._description = desc
        self._hidden = is_hidden
        self._generator = cmake_generator
        self._binary_dir = binary_path
        self._install_dir = install_path
        self._cache_variables = cache_vars if cache_vars else {}
        self._env_variables = env_vars if env_vars else {}
        if inherits is None:
            self._base_presets = []
        elif isinstance(inherits, Preset):
            self._base_presets = [inherits]
        else:
            self._base_presets = list(inherits)
        self._is_full_preset = is_full_preset


    @property
    def preset_name(self) -> str:
        """
        Gets the name of the preset.
        """
        return self._name


    @property
    def description(self) -> Optional[str]:
        """
        Gets the description of the preset.
        """
        return self._description


    @description.setter
    def description(self, value: Optional[str]) -> None:
        """
        Sets the description of the preset.
        """
        self._description = value


    @property
    def hidden(self) -> bool:
        """
        Gets whether the preset should be hidden.
        """
        return self._hidden


    @hidden.setter
    def hidden(self, value: bool) -> None:
        """
        Sets whether the preset should be hidden.
        """
        self._hidden = value


    @property
    def generator(self) -> Optional[str]:
        """
        Gets the name of the CMake generator.
        """
        return self._generator


    @generator.setter
    def generator(self, value: Optional[str | ECMakeGenerator]) -> None:
        """
        Sets the name of the CMake generator.
        """
        if value is None:
            self._generator = None
        elif isinstance(value, ECMakeGenerator):
            self._generator = value.value
        else:
            self._generator = str(value)


    @property
    def binary_dir(self) -> Optional[str]:
        """
        Gets the path to the directory where CMake will generate the build files.
        """
        return self._binary_dir


    @binary_dir.setter
    def binary_dir(self, value: Optional[str]) -> None:
        """
        Sets the path to the directory where CMake will generate the build files.
        """
        self._binary_dir = value


    @property
    def install_dir(self) -> Optional[str]:
        """
        Gets the path to the directory where CMake will install built targets.
        """
        return self._install_dir


    @install_dir.setter
    def install_dir(self, value: Optional[str]) -> None:
        """
        Sets the path to the directory where CMake will install built targets.
        """
        self._install_dir = value


    @property
    def cache_variables(self) -> Dict[str, str]:
        """
        Gets the dictionary of cache variables to set.
        """
        return self._cache_variables


    @property
    def cmake_build_type(self) -> Optional[str]:
        """
        Gets the CMake build type.
        """
        if Preset.CMAKE_BUILD_TYPE_VAR in self._cache_variables:
            return self._cache_variables[Preset.CMAKE_BUILD_TYPE_VAR]
        return None


    @cmake_build_type.setter
    def cmake_build_type(self, value: Optional[str | ECMakeBuildType]) -> None:
        """
        Sets the CMake build type.
        """
        if value is None:
            if Preset.CMAKE_BUILD_TYPE_VAR in self._cache_variables:
                del self._cache_variables[Preset.CMAKE_BUILD_TYPE_VAR]
        elif isinstance(value, ECMakeBuildType):
            self._cache_variables[Preset.CMAKE_BUILD_TYPE_VAR] = value.value
        else:
            self._cache_variables[Preset.CMAKE_BUILD_TYPE_VAR] = value


    @property
    def env_variables(self) -> Dict[str, str]:
        """
        Gets the dictionary of environment variables to set.
        """
        return self._env_variables


    def as_build_preset(self,
        source_dir: Path,
        generated_dir: Path) -> Dict[str, object]:
        """
        Converts the preset to a CMake build preset.
        @param source_dir Path to the root of the PyMake project.
        @param generated_dir Path to the directory where PyMake will generate
          CMake files.
        @return A dictionary representing the preset as a CMake build preset.
          This dictionary can be serialized to JSON and written to the
          "buildPresets" section of a CMakePresets.json file.
        """
        preset: Dict[str, object] = {}
        preset["name"] = self._name
        if self._description is not None:
            preset["description"] = self._description
        if self._hidden:
            preset["hidden"] = True
        preset["configurePreset"] = self._name
        preset["inheritConfigureEnvironment"] = True
        preset["targets"] = "install"
        return preset


    def as_configure_preset(self,
        source_dir: Path,
        generated_dir: Path) -> Dict[str, object]:
        """
        Converts the preset to a CMake configure preset.
        @param source_dir Path to the root of the PyMake project.
        @param generated_dir Path to the directory where PyMake will generate
          CMake files.
        @return A dictionary representing the preset as a CMake configure
          preset. This dictionary can be serialized to JSON and written to the
          "configurePresets" section of a CMakePresets.json file.
        """
        # Resolve paths into absolute paths
        if self._binary_dir and not Path(self._binary_dir).is_absolute():
            binary_dir = str(source_dir / self._binary_dir)
        elif self._binary_dir:
            binary_dir = self._binary_dir
        else:
            binary_dir = None

        if self._install_dir and not Path(self._install_dir).is_absolute():
            install_dir = str(source_dir / self._install_dir)
        elif self._install_dir:
            install_dir = self._install_dir
        else:
            install_dir = None

        preset: Dict[str, object] = {}
        preset["name"] = self._name
        if self._description is not None:
            preset["description"] = self._description
        if self._hidden:
            preset["hidden"] = True
        if self._generator is not None:
            preset["generator"] = self._generator
        if binary_dir is not None:
            preset["binaryDir"] = binary_dir
        if install_dir is not None:
            preset["installDir"] = install_dir
        if self._cache_variables:
            preset["cacheVariables"] = self._cache_variables
        if self._env_variables:
            preset["environment"] = self._env_variables
        if self._base_presets:
            preset["inherits"] = [p._name for p in self._base_presets]
        return preset


    def as_full_preset(self) -> Preset:
        """
        Rolls all values from inherited presets into a new preset.
        The preset generated by this method will contain all values from this
          preset and all of its inherited presets. Precedence is given to values
          from presets farther down the inheritance chain.
        @return The preset with all values rolled into it.
        """
        # Start with a preset that has values not modified by `_merge` set to
        #   this preset's values
        preset = Preset(
            name=self._name,
            desc=self._description,
            inherits=self._base_presets,
            is_full_preset=True
        )
        for p in self._base_presets:
            preset.merge(p)
        preset.merge(self)

        return preset


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
        full_preset = self.as_full_preset()
        props: Dict[str, object] = {}
        props["description"] = full_preset._description
        props["hidden"] = full_preset._hidden
        props["generator"] = full_preset._generator
        props["binaryDir"] = full_preset._binary_dir
        props["installDir"] = full_preset._install_dir
        props["cacheVariables"] = full_preset._cache_variables
        props["environment"] = full_preset._env_variables
        props["inherits"] = [p._name for p in full_preset._base_presets]
        generator.write_file({
            full_preset.preset_name: props
        }, output_path)


    def inherit_from(self, preset: Preset) -> None:
        """
        Inherit from another preset.
        @param preset Preset to inherit from.
        """
        self._base_presets.append(preset)


    def merge(self, preset: Preset) -> None:
        """
        Merges the values of another preset into this preset.
        @param preset Preset to merge.
        """
        if preset._hidden:
            self._hidden = True
        if preset._generator is not None:
            self._generator = preset._generator
        if preset._binary_dir is not None:
            self._binary_dir = preset._binary_dir
        if preset._install_dir is not None:
            self._install_dir = preset._install_dir
        self._cache_variables.update(preset._cache_variables)
        self._env_variables.update(preset._env_variables)


    def set_cache_variable(self, name: str, value: str) -> None:
        """
        Sets a CMake cache variable.
        @param name Name of the cache variable.
        @param value Value of the cache variable.
        """
        self._cache_variables[name] = value


    def set_env_variable(self, name: str, value: str) -> None:
        """
        Sets an environment variable.
        @param name Name of the environment variable.
        @param value Value of the environment variable.
        """
        self._env_variables[name] = value
