from __future__ import annotations
from pymake.common.target_type import ETargetType
from pymake.core.build_script_set import BuildScriptSet
from pymake.targets.target import ITarget

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


    def generate_declaration(self) -> None:
        """
        Generates the CMake code that declares the target.
        """
        # Generate the CMake code
        generator = self._build_scripts.get_or_add_build_script().generator
        with generator.open_method_block("add_executable") as b:
            b.add_arguments(self._target_name)
