from pymake.core.build_script import BuildScript
from pymake.data.executable_target import ExecutableTarget
from pymake.data.valgrind_test_target import ValgrindTestTarget

class MemcheckTestTarget(ValgrindTestTarget):
    """
    Represents a Valgrind memcheck test target.
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
            target_executable
        )


    def _generate_test_declaration(self,
        build_script: BuildScript) -> None:
        """
        Generates the CMake code to add test target.
        @param build_script Build script to write the target to.
        """
        with build_script.generator.open_method_block("add_test") as b:
            b.add_keyword_arguments("NAME", self._target_name)
            b.add_keyword_arguments(
                "COMMAND",
                "valgrind",
                "--leak-check=full",
                "--track-origins=yes",
                "--fair-sched=yes",
                "--show-leak-kinds=definite,indirect,possible",
                "--errors-for-leak-kinds=definite,indirect,possible",
                "--error-exitcode=1",
                # TODO: If the target is installed, get the path of the target
                # from the install directory. If the target is not installed,
                # get the path of the target from the build directory.
                f"./{self._target_exe.target_name}"
            )
