from pymake.model.project_scope import ProjectScope
from pymake.model.pymake_project import PyMakeProject
from pymake.views.target_set_view import TargetSetView
from typing import Optional

class ProjectScopeView:
    """
    Provides an interface for modifying a PyMake project scope.
    """
    def __init__(self,
        project: PyMakeProject,
        project_scope: ProjectScope):
        """
        Initializes the project scope view.
        @param project The project that the project scope is in.
        @param project_scope The project scope to provide a view for.
        """
        self._project = project
        self._project_scope = project_scope


    def create_target_set(self,
        set_name: str,
        all_target_name: Optional[str] = None,
        all_suffix: str = "-all",
        test_target_name: Optional[str] = None,
        test_suffix: str = "-test",
        common_target_name: Optional[str] = None,
        common_suffix: str = "-common") -> TargetSetView:
        """
        Creates a new target set.
        @param set_name The name of the target set.
        @param all_target_name Name of the target set-specific `all` target. If
          `None`, the target set's `all` target will be named
          `[set_name][all_suffix]`.
        @param all_suffix Suffix to append to the target set name to generate
          the target set's `all` target name. Only used if `all_target_name` is
          `None`.
        @param test_target_name Name of the target set-specific `test` target.
          If `None`, the target set's `test` target will be named
          `[set_name][test_suffix]`.
        @param test_suffix Suffix to append to the target set name to generate
          the target set's `test` target name. Only used if `test_target_name`
          is `None`.
        @param common_target_name Name of the target set-specific `common`
          target. If `None`, the target set's `common` target will be named
          `[set_name][common_suffix]`.
        @param common_suffix Suffix to append to the target set name to
          generate the target set's `common` target name. Only used if
          `common_target_name` is `None`.
        @throws RuntimeError Thrown if the target set already exists with the
          same name and was declared at a different location.
        @returns The view for the target set.
        """
        # Determine the target set's `all` target name.
        if all_target_name is None:
            all_target_name = f"{set_name}{all_suffix}"

        # Determine the target set's `test` target name.
        if test_target_name is None:
            test_target_name = f"{set_name}{test_suffix}"

        # Determine the target set's `common` target name.
        if common_target_name is None:
            common_target_name = f"{set_name}{common_suffix}"

        return TargetSetView(
            self._project,
            self._project_scope,
            self._project_scope.add_target_set(
                set_name,
                all_target_name,
                test_target_name,
                common_target_name
            )
        )
