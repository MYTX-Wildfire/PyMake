from pymake.common.sanitizer_flags import ESanitizerFlags
from pymake.model.project_scope import ProjectScope
from pymake.model.pymake_project import PyMakeProject
from pymake.model.target_set import TargetSet
from pymake.views.build_target_view import BuildTargetView

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
