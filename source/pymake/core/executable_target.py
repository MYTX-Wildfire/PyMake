from __future__ import annotations
from pymake.common.target_type import ETargetType
from pymake.core.build_script_set import BuildScriptSet
from pymake.core.target import ITarget

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

        # Generate the CMake code
        generator = self._build_scripts.get_or_add_build_script().generator
        with generator.open_method_block("add_executable") as b:
            b.add_arguments(self._target_name)


    def get_full_target(self) -> ExecutableTarget:
        """
        Gets a target instance that includes all values for the target.
        Target instances normally do not include values from targets that
          they link to. The target instance returned by this method contains
          all values for the target, including values from linked-to targets.
        @returns A target instance that includes all values from targets that
          this target links to.
        """
        # Nothing needs to be done yet since target linking hasn't been
        #   implemented yet
        return self
