from pymake.core.build_script_set import BuildScriptSet
from pymake.targets.target import ITarget
from pymake.targets.test_target import TestTarget

class GoogleTestTarget(TestTarget):
    """
    Represents an GoogleTest executable to be added to the `test` target.
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
            project_all_target_name,
            project_test_target_name,
            test_build_fixture
        )


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
        return GoogleTestTarget(
            self._build_scripts,
            self._target_name,
            self._project_all_target_name,
            self._project_test_target_name,
            self._test_build_fixture
        )
