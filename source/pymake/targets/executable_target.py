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
        target_name: str,
        project_all_target_name: str):
        """
        Initializes the target.
        @param build_scripts Set of build scripts that the project will generate.
        @param target_name Name of the target.
        @param project_all_target_name Name of the project's `all` target.
        """
        super().__init__(
            build_scripts,
            target_name,
            ETargetType.EXECUTABLE
        )
        self._project_all_target_name = project_all_target_name

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

        # Add the target as a dependency of the project's `all` target
        with generator.open_method_block("add_dependencies") as b:
            b.add_arguments(self._project_all_target_name)
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


    def mark_is_test_target(
        self,
        add_valgrind_target: bool = False,
        valgrind_target_suffix: str = "valgrind",
        add_helgrind_target: bool = False,
        helgrind_target_suffix: str = "helgrind",
        add_drd_target: bool = False,
        drd_target_suffix: str = "drd"):
        """
        Marks the target as a test target.
        @param add_valgrind Whether to also add a valgrind test target that runs
          the executable.
        @param valgrind_target_suffix Suffix to add to the target name to
          generate the valgrind target name.
        @param add_helgrind Whether to also add a helgrind test target that runs
          the executable.
        @param helgrind_target_suffix Suffix to add to the target name to
          generate the helgrind target name.
        @param add_drd Whether to also add a valgrind drd test target that runs
          the executable.
        """
        self._is_test_target = Traced(True)
        generator = self._build_scripts.get_or_add_build_script().generator
        with generator.open_method_block("add_test") as b:
            b.add_keyword_arguments("NAME", self._target_name)
            b.add_keyword_arguments("COMMAND", self._target_name)

        if add_valgrind_target:
            valgrind_target = f"{self._target_name}-{valgrind_target_suffix}"
            with generator.open_method_block("add_test") as b:
                b.add_keyword_arguments("NAME", valgrind_target)
                b.add_keyword_arguments(
                    "COMMAND",
                    "valgrind",
                    "--leak-check=full",
                    "--track-origins=yes",
                    "--fair-sched=yes",
                    "--show-leak-kinds=definite,indirect,possible",
                    "--errors-for-leak-kinds=definite,indirect,possible",
                    "--error-exitcode=1",
                    f"./{self._target_name}"
                )

        if add_helgrind_target:
            helgrind_target = f"{self._target_name}-{helgrind_target_suffix}"
            with generator.open_method_block("add_test") as b:
                b.add_keyword_arguments("NAME", helgrind_target)
                b.add_keyword_arguments(
                    "COMMAND",
                    "valgrind",
                    "--tool=helgrind",
                    "--fair-sched=yes",
                    "--error-exitcode=1",
                    f"./{self._target_name}"
                )

        if add_drd_target:
            drd_target = f"{self._target_name}-{drd_target_suffix}"
            with generator.open_method_block("add_test") as b:
                b.add_keyword_arguments("NAME", drd_target)
                b.add_keyword_arguments(
                    "COMMAND",
                    "valgrind",
                    "--tool=drd",
                    "--fair-sched=yes",
                    "--error-exitcode=1",
                    f"./{self._target_name}"
                )


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
            self._target_name,
            self._project_all_target_name
        )
        target._install_rpath = self._install_rpath
        return target
