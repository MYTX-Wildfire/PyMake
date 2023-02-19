from __future__ import annotations
from pathlib import Path
from typing import Dict, NamedTuple, Optional

class PresetState(NamedTuple):
    """
    Contains all values that may be set by a preset.
    """
    # Name of the preset that generated the state data
    preset_name: str

    # Path to the directory to use as the build directory.
    # @invariant This will always be an absolute path.
    binary_dir: Optional[Path]

    # Path to the directory to use as the install directory.
    # @invariant This will always be an absolute path.
    install_dir: Optional[Path]

    # Path to the directory containing the generated CMake build scripts.
    # @invariant This will always be an absolute path.
    generated_dir: Path

    # Path to the directory containing the PyMake project.
    # @warning This value is **NOT** the same as a CMake source directory value.
    #   This will be the path to the folder containing source files and PyMake
    #   build scripts. To get the folder where generated CMake build scripts
    #   were written, use `generated_dir`.
    # @invariant This will always be an absolute path.
    source_dir: Path

    # Generator that CMake should use.
    # @warning This must be a value recognized by CMake. PyMake will not attempt
    #   to validate this value.
    generator: Optional[str]

    # Dictionary of variables to pass to CMake.
    # Each entry in this dictionary will be a variable name and the value to
    #   assign to the variable.
    variables: Dict[str, str]

    # Dictionary of environment variables to use when invoking CMake.
    # Each entry in this dictionary will be a variable name and the value to
    #   assign to the variable.
    env_variables: Dict[str, str]

    def apply(self, other: PresetState) -> PresetState:
        """
        Applies the given preset state on top of the current preset state.
        This method is used to "merge" two preset state instances together. The
          passed in preset state will take precedence over the current preset
          state to this method and will overwrite values in the current preset
          state if the two preset states set the same variables to different
          values.
        @param other Preset state instance to apply on top of the current preset
          state instance.
        @returns A new preset state instance containing values from the current
          preset state and the applied preset state.
        """
        # Create new instances of the current preset state's collections
        vars = self.variables.copy()
        vars.update(other.variables)
        env_vars = self.env_variables.copy()
        env_vars.update(other.env_variables)

        return PresetState(
            # These values will always exist in both preset state instances.
            #   Use the values from the passed in preset state instance since
            #   it has precedence over the current instance.
            preset_name=other.preset_name,
            generated_dir=other.generated_dir,
            source_dir=other.source_dir,
            # Merge these values, giving precedence to the passed in preset
            #   state instance
            binary_dir=other.binary_dir if other.binary_dir else self.binary_dir,
            install_dir=other.install_dir if other.install_dir else self.install_dir,
            generator=other.generator if other.generator else self.generator,
            variables=vars,
            env_variables=env_vars
        )
