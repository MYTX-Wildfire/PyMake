from pymake.common.test_flags import ETestFlags
from pymake.core.build_script import BuildScript
from pymake.model.targets.build.executable_target import ExecutableTarget

class TestTarget(ExecutableTarget):
    """
    Represents a test executable target.
    """
    def __init__(self,
        target_name: str,
        test_flags: int,
        sanitizer_flags: int):
        """
        Initializes the target.
        @param target_name The name of the target.
        @param test_flags Flags to set for the test target. Must have at least
          one flag set.
        @param sanitizer_flags The sanitizers enabled for the target.
        @throws RuntimeError If no test flags are set.
        """
        super().__init__(
            target_name,
            test_flags,
            sanitizer_flags
        )

        if test_flags == ETestFlags.NONE:
            raise RuntimeError(
                f"Test target '{target_name}' must have at least one test " + \
                "flag set"
            )


    def _generate_test_declaration(self,
        build_script: BuildScript) -> None:
        """
        Generates the CMake code to add test target.
        @param build_script Build script to write the target to.
        """
        raise NotImplementedError()
