from pymake.model.targets.build.executable_target import ExecutableTarget
from pymake.model.targets.test.test_wrapper_target import TestWrapperTarget

class ValgrindTestTarget(TestWrapperTarget):
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
            target_executable.sanitizer_flags,
            target_executable
        )
