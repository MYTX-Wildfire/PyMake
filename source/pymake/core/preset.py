from __future__ import annotations
from pathlib import Path
from pymake.core.preset_state import PresetState
from pymake.helpers.caller_info import CallerInfo
from pymake.helpers.path_statics import to_abs_path
from typing import Dict, List

class Preset:
    """
    Represents a preset series of option values to use when building.
    PyMake presets are *not* directly equivalent to CMake presets. With CMake
      presets, developers must specify exactly one preset when they build their
      project. With PyMake presets, developers can specify *multiple* presets
      when building, which will merge the settings from all specified presets
      into a single build. This allows settings to mixed and matched easily when
      values are independent of each other, such as when specifying a CPU
      architecture preset and build type preset.
    @remarks Developers can still use PyMake presets the same way as CMake
      presets by implementing a preset that inherits from other presets.
    """
    def __init__(self,
        preset_name: str,
        source_dir: Path,
        generated_dir: Path,
        caller_offset: int):
        """
        Initializes the object.
        @param preset_name Name given to the preset. Must be unique within a
          PyMake project.
        @param source_dir Directory containing the project's source files and
          PyMake build scripts. Must be an absolute path.
        @param generated_dir Directory where PyMake will generate the CMake
          build scripts. Must be an absolute path.
        @throws ValueError Thrown if any parameter is invalid.
        """
        # Validate method arguments
        if not preset_name:
            raise ValueError("A project name string may not be empty.")
        elif preset_name.isspace():
            raise ValueError("A project's name cannot be only whitespace.")

        # Preset state instance containing only values added to this preset.
        #   This state instance does **not** contain values that are inherited.
        self._state = PresetState(
            preset_name=preset_name,
            binary_dir=None,
            install_dir=None,
            generated_dir=generated_dir,
            source_dir=source_dir,
            generator=None,
            variables={},
            env_variables={}
        )
        self._call_site = CallerInfo(caller_offset + 1)

        # Dictionary of presets that this preset inherits from.
        # Each preset is indexed by its name.
        self._base_presets: Dict[str, Preset] = {}

        # Store presets in the order they were added
        # This is necessary because presets must be applied in the order they
        #   were added. This ensures that conflicts between presets are resolved
        #   deterministically and can be adjusted by developers.
        self._base_preset_order: List[Preset] = []

    @property
    def call_site(self) -> CallerInfo:
        """
        @brief Gets the location in the project's PyMake build scripts where the
          preset was defined.
        """
        return self._call_site

    @property
    def preset_name(self) -> str:
        """
        Gets the name assigned to the preset.
        """
        return self._state.preset_name

    @property
    def preset_state(self) -> PresetState:
        """
        Generates the CMake values to set when applying this preset.
        """
        # Start with the state from the first preset to inherit from, then apply
        #   each subsequent inherited preset on top of it
        state = (self._base_preset_order[0].preset_state
            if self._base_preset_order else self._state)
        for p in self._base_preset_order:
            state = state.apply(p.preset_state)

        # Lastly, apply the current preset's state on top of the inherited
        #   presets' state
        state = state.apply(self._state)
        return state

    def set_build_dir(self, path: str | Path) -> None:
        """
        Sets the path that CMake should use as the build/binary directory.
        @param path Path of the build directory to use. If this is a relative
          path, the path will be interpreted relative to the source tree's root.
        """
        build_dir = to_abs_path(
            Path(path),
            self._state.source_dir
        )
        self._state = self._state._replace(
            binary_dir=build_dir
        )

    def set_env_variable(self, env_var: str, value: object) -> None:
        """
        Sets an environment variable to set when invoking CMake via the preset.
        @param env_var Name of the environment variable to set.
        @param value Value to pass as the value of the environment variable.
        """
        self._state.env_variables[env_var] = str(value)

    def set_generator(self, generator: str) -> None:
        """
        Sets the generator that should be used.
        @param generator Name of the generator to use. This must be a value that
          is recognized by CMake.
        """
        self._state = self._state._replace(
            generator=generator
        )

    def set_install_dir(self, path: str | Path) -> None:
        """
        Sets the path that CMake should use as the install directory.
        @param path Path of the install directory to use. If this is a relative
          path, the path will be interpreted relative to the source tree's root.
        """
        install_dir = to_abs_path(
            Path(path),
            self._state.source_dir
        )
        self._state = self._state._replace(
            install_dir=install_dir
        )

    def set_variable(self, cmake_var: str, value: object) -> None:
        """
        Sets a CMake variable to pass to CMake when using the preset.
        @param cmake_var Name of the CMake variable to set.
        @param value Value to pass to CMake as the value of the variable.
        @returns `self`
        """
        self._state.variables[cmake_var] = str(value)

    def inherit_from(self, preset: Preset) -> None:
        """
        Configures the preset to inherit all values from the given preset.
        @warning PyMake presets use **late-binding**. This means that if you
          call this method and then modify the base preset, the derived preset
          will still reflect those changes.
        @param preset Preset to inherit from.
        """
        self._base_presets[preset.preset_name] = preset
        self._base_preset_order.append(preset)
