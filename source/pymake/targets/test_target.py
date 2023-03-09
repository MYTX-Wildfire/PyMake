from pymake.core.build_script_set import BuildScriptSet
from pymake.targets.executable_target import ExecutableTarget
from pymake.targets.target import ITarget

class TestTarget(ExecutableTarget):
    """
    Represents an executable to be added to the `test` target.
    """
    def __init__(self,
        build_scripts: BuildScriptSet,
        target_name: str,
        project_all_target_name: str,
        project_test_target_name: str,
        test_build_fixture: str):
        """
        Initializes the target.
        @param build_scripts Set of build scripts that the project will generate.
        @param target_name Name of the target.
        @param project_all_target_name Name of the project's `all` target.
        @param project_test_target_name Name of the project's `test` target.
        @param test_build_fixture Name of the fixture that forces test targets
          to be built.
        """
        super().__init__(
            build_scripts,
            target_name,
            project_all_target_name
        )
        self._test_build_fixture = test_build_fixture
        self._project_test_target_name = project_test_target_name


    def generate_declaration(self) -> None:
        """
        Generates the CMake code that declares the target.
        """
        # Generate the executable target declaration first
        super().generate_declaration()

        # Add the target as a test target
        generator = self._build_scripts.get_or_add_build_script().generator
        with generator.open_method_block("add_test") as b:
            b.add_keyword_arguments("NAME", self._target_name)
            b.add_keyword_arguments("COMMAND", self._target_name)

        # This must be present in the same file that declares the target
        #   (or one where the test target is visible, which is not the case
        #   for the top-level CMakeLists.txt file if the target is declared
        #   in a subdirectory).
        with generator.open_method_block("set_tests_properties") as b:
            b.add_arguments(self.target_name)
            b.add_arguments("PROPERTIES")
            b.add_keyword_arguments(
                "FIXTURES_REQUIRED",
                self._test_build_fixture
            )

        # Add the target as a dependency of the project's `test` target
        with generator.open_method_block("add_dependencies") as b:
            b.add_arguments(self._project_test_target_name)
            b.add_arguments(self._target_name)


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
        return TestTarget(
            self._build_scripts,
            self._target_name,
            self._project_all_target_name,
            self._project_test_target_name,
            self._test_build_fixture
        )
