from pymake.core.build_script import BuildScript
from pymake.model.targets.build.executable_target import ExecutableTarget
from pymake.model.targets.test.test_target import TestTarget

class ValgrindTestTarget(TestTarget):
    """
    Represents a Valgrind-based test target.
    """
    def __init__(self,
        target_name: str,
        test_flags: int,
        target_executable: ExecutableTarget):
        """
        Initializes the target.
        @param target_name The name of the target.
        @param test_flags Flags to set for the test target. Must have at least
          one flag set.
        @param target_executable The executable target to run under Valgrind.
        @throws RuntimeError If no test flags are set.
        """
        super().__init__(
            target_name,
            test_flags,
            target_executable.sanitizer_flags
        )
        self._target_exe = target_executable


    def _generate_declaration(self,
        build_script: BuildScript) -> None:
        """
        Generates the CMake code for the declaration of the target.
        @param build_script Build script to write the target to.
        """
        # Do nothing - Valgrind targets do not need to be declared since they
        #   use an existing executable target
        pass
