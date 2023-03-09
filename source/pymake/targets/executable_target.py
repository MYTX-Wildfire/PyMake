from __future__ import annotations
from pymake.common.target_type import ETargetType
from pymake.core.build_script_set import BuildScriptSet
from pymake.targets.target import ITarget
from pymake.tracing.traced import Traced
from typing import Dict, Optional

class ExecutableTarget(ITarget):
    """
    Represents a single executable CMake target.
    """
    def __init__(self,
        build_scripts: BuildScriptSet,
        target_name: str):
        """
        Initializes the target.
        @param build_scripts Set of build scripts that the project will generate.
        @param target_name Name of the target.
        """
        super().__init__(
            build_scripts,
            target_name,
            ETargetType.EXECUTABLE
        )

        # Whether the target is a test target
        self._is_test_target = Traced(False)

        # RPATH to use when installed
        self._install_rpath: Optional[Traced[str]] = None


    def generate_declaration(self) -> None:
        """
        Generates the CMake code that declares the target.
        """
        # Generate the CMake code
        generator = self._build_scripts.get_or_add_build_script().generator
        with generator.open_method_block("add_executable") as b:
            b.add_arguments(self._target_name)


    def generate_trace_dict(self) -> Dict[str, object]:
        """
        Generates a dictionary containing the properties of the target.
        @return Dictionary containing the properties of the target.
        """
        # Get the trace file from the `Target` class
        trace_dict = super().generate_trace_dict()

        # Add executable-specific properties
        if self._install_rpath is not None:
            trace_dict["install_rpath"] = self._install_rpath

        return trace_dict


    def mark_is_test_target(self):
        """
        Marks the target as a test target.
        """
        self._is_test_target = Traced(True)
        generator = self._build_scripts.get_or_add_build_script().generator
        with generator.open_method_block("add_test") as b:
            b.add_keyword_arguments("NAME", self._target_name)
            b.add_keyword_arguments("COMMAND", self._target_name)


    def set_install_rpath(self, path: str) -> None:
        """
        Sets the rpath that the installed executable will use.
        @param path Path to set the rpath to. Can use `$ORIGIN`.
        """
        self._install_rpath = Traced(path)
        generator = self._build_scripts.get_or_add_build_script().generator
        with generator.open_method_block("set_target_properties") as b:
            b.add_arguments(self._target_name)
            b.add_arguments("PROPERTIES")
            b.add_keyword_arguments("INSTALL_RPATH", path)


    def _create_empty_clone(self) -> ITarget:
        """
        Creates an empty clone of the target.
        An empty clone is a clone that has only the values required to be passed
          to the target's constructor and not any values passed to any of the
          target's methods.
        @remarks This method is only used to ensure that `_get_full_target()`
          can construct a clone of the current target and add properties to
          the clone.
        @returns An empty clone of the target.
        """
        target = ExecutableTarget(
            self._build_scripts,
            self._target_name
        )
        target._install_rpath = self._install_rpath
        return target
