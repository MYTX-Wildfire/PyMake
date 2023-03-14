from pymake.common.sanitizer_flags import ESanitizerFlags
from pymake.model.project_scope import ProjectScope
from pymake.model.pymake_project import PyMakeProject
from pymake.model.target_set import TargetSet
from pymake.model.targets.build.executable_target import ExecutableTarget
from pymake.views.build_target_view import BuildTargetView
from pymake.views.imported_target_view import ImportedTargetView
from pymake.views.valgrind_target_view import ValgrindTargetView

class TargetSetView:
    """
    Provides an interface for modifying a PyMake target set.
    """
    def __init__(self,
        project: PyMakeProject,
        project_scope: ProjectScope,
        target_set: TargetSet):
        """
        Initializes the target set view.
        @param project The project that the target set's project scope belongs to.
        @param project_scope The project scope that the target set belongs to.
        @param target_set The target set to provide a view for.
        """
        self._project = project
        self._project_scope = project_scope
        self._target_set = target_set


    def add_executable(self,
        target_name: str,
        sanitizer_flags: int = ESanitizerFlags.NONE) -> BuildTargetView:
        """
        Adds a non-test executable target to the target set.
        @param target_name The name of the target.
        @param sanitizer_flags The sanitizers enabled for the target.
        @throws RuntimeError Thrown if a target with the same name already
          exists and was added at a different location.
        @returns A view for the target.
        """
        return BuildTargetView(
            self._project,
            self._project_scope,
            self._target_set,
            self._target_set.add_executable(
                target_name,
                sanitizer_flags
            )
        )


    def add_external_static_library(self,
        target_name: str,
        sanitizer_flags: int = ESanitizerFlags.NONE) -> ImportedTargetView:
        """
        Adds an external static library target to the target set.
        @param target_name The name of the target.
        @param sanitizer_flags The sanitizers enabled for the target.
        @throws RuntimeError Thrown if a target with the same name already
          exists and was added at a different location.
        @returns A view for the target.
        """
        return ImportedTargetView(
            self._project,
            self._project_scope,
            self._target_set,
            self._target_set.add_external_static_library(
                target_name,
                sanitizer_flags
            )
        )


    def add_drd_target(self,
        test_target_name: str,
        wrapped_target: BuildTargetView) -> ValgrindTargetView:
        """
        Adds a DRD test executable target to the target set.
        @param test_target_name The name of the test target that runs the
          executable under Valgrind.
        @param wrapped_target The executable target that is wrapped by Valgrind.
        @throws RuntimeError Thrown if the wrapped target is not an executable
          target.
        @returns A view for the target.
        """
        if not isinstance(wrapped_target.target, ExecutableTarget):
            raise RuntimeError(
                "The wrapped target must be an executable target."
            )

        return ValgrindTargetView(
            self._project,
            self._project_scope,
            self._target_set,
            self._target_set.add_drd_target(
                test_target_name,
                wrapped_target.target
            )
        )


    def add_gtest_executable(self,
        target_name: str,
        test_flags: int,
        sanitizer_flags: int = ESanitizerFlags.NONE) -> BuildTargetView:
        """
        Adds a GoogleTest test executable target to the target set.
        @param target_name The name of the target.
        @param test_flags The test flags for the target.
        @param sanitizer_flags The sanitizers enabled for the target.
        @throws RuntimeError Thrown if a target with the same name already
          exists and was added at a different location.
        @returns A view for the target.
        """
        return BuildTargetView(
            self._project,
            self._project_scope,
            self._target_set,
            self._target_set.add_gtest_executable(
                target_name,
                test_flags,
                sanitizer_flags
            )
        )


    def add_helgrind_target(self,
        test_target_name: str,
        wrapped_target: BuildTargetView) -> ValgrindTargetView:
        """
        Adds a Helgrind test executable target to the target set.
        @param test_target_name The name of the test target that runs the
          executable under Valgrind.
        @param wrapped_target The executable target that is wrapped by Valgrind.
        @throws RuntimeError Thrown if the wrapped target is not an executable
          target.
        @returns A view for the target.
        """
        if not isinstance(wrapped_target.target, ExecutableTarget):
            raise RuntimeError(
                "The wrapped target must be an executable target."
            )

        return ValgrindTargetView(
            self._project,
            self._project_scope,
            self._target_set,
            self._target_set.add_helgrind_target(
                test_target_name,
                wrapped_target.target
            )
        )


    def add_memcheck_target(self,
        test_target_name: str,
        wrapped_target: BuildTargetView) -> ValgrindTargetView:
        """
        Adds a Memcheck test executable target to the target set.
        @param test_target_name The name of the test target that runs the
          executable under Valgrind.
        @param wrapped_target The executable target that is wrapped by Valgrind.
        @throws RuntimeError Thrown if the wrapped target is not an executable
          target.
        @returns A view for the target.
        """
        if not isinstance(wrapped_target.target, ExecutableTarget):
            raise RuntimeError(
                "The wrapped target must be an executable target."
            )

        return ValgrindTargetView(
            self._project,
            self._project_scope,
            self._target_set,
            self._target_set.add_memcheck_target(
                test_target_name,
                wrapped_target.target
            )
        )


    def add_shared_library(self,
        target_name: str,
        sanitizer_flags: int = ESanitizerFlags.NONE) -> BuildTargetView:
        """
        Adds a library target to the target set.
        @param target_name The name of the target.
        @param sanitizer_flags The sanitizers enabled for the target.
        @throws RuntimeError Thrown if a target with the same name already
          exists and was added at a different location.
        @returns A view for the target.
        """
        return BuildTargetView(
            self._project,
            self._project_scope,
            self._target_set,
            self._target_set.add_shared_library(
                target_name,
                sanitizer_flags
            )
        )


    def add_static_library(self,
        target_name: str,
        sanitizer_flags: int = ESanitizerFlags.NONE) -> BuildTargetView:
        """
        Adds a library target to the target set.
        @param target_name The name of the target.
        @param sanitizer_flags The sanitizers enabled for the target.
        @throws RuntimeError Thrown if a target with the same name already
          exists and was added at a different location.
        @returns A view for the target.
        """
        return BuildTargetView(
            self._project,
            self._project_scope,
            self._target_set,
            self._target_set.add_static_library(
                target_name,
                sanitizer_flags
            )
        )
