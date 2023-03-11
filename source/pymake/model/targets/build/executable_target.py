from pymake.common.target_type import ETargetType
from pymake.core.build_script import BuildScript
from pymake.model.targets.build.build_target import BuildTarget

class ExecutableTarget(BuildTarget):
    """
    Represents an executable target.
    """
    def __init__(self,
        target_name: str,
        test_flags: int,
        sanitizer_flags: int):
        """
        Initializes the target.
        @param target_name The name of the target.
        @param test_flags Identifies whether the target is a test target and
          what kind of target the test target is.
        @param sanitizer_flags The sanitizers enabled for the target.
        """
        super().__init__(
            target_name,
            ETargetType.EXECUTABLE,
            test_flags,
            sanitizer_flags
        )


    def _generate_declaration(self,
        build_script: BuildScript) -> None:
        """
        Generates the CMake code for the declaration of the target.
        @param build_script Build script to write the target to.
        """
        with build_script.generator.open_method_block("add_executable") as b:
            b.add_arguments(self.target_name)
