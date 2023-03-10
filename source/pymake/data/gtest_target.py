from pymake.core.build_script import BuildScript
from pymake.data.test_target import TestTarget

class GTestTarget(TestTarget):
    """
    Represents a GoogleTest test executable target.
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


    def _generate_test_declaration(self,
        build_script: BuildScript) -> None:
        """
        Generates the CMake code to add test target.
        @param build_script Build script to write the target to.
        """
        with build_script.generator.open_method_block("add_test") as b:
            b.add_keyword_arguments("NAME", self._target_name)
            b.add_keyword_arguments("COMMAND", self._target_name)
