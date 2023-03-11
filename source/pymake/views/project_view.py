from pymake.common.project_language import EProjectLanguage
from pymake.model.pymake_project import PyMakeProject
from pymake.views.project_scope_view import ProjectScopeView
from typing import Iterable, Optional

class ProjectView:
    """
    Provides an interface for modifying a PyMake project.
    """
    def __init__(self, project: PyMakeProject):
        """
        Initializes the project view.
        @param project The project to provide a view for.
        """
        self._project = project


    def create_project_scope(self,
        project_name: str,
        project_languages: EProjectLanguage | Iterable[EProjectLanguage],
        project_all_target_name: Optional[str] = None,
        project_all_suffix: str = "-all",
        project_test_target_name: Optional[str] = None,
        project_test_suffix: str = "-test") -> ProjectScopeView:
        """
        Creates a new project scope.
        @param project_name The name of the project.
        @param project_languages The languages used in the project.
        @param enable_ctest Whether to enable CTest for the project.
        @param project_all_target_name Name of the project-specific `all`
          target. If `None`, the project's `all` target will be named
          `[project_name][project_all_suffix]`.
        @param project_all_suffix Suffix to append to the project name to
          generate the project's `all` target name. Only used if
          `project_all_target_name` is `None`.
        @param project_test_target_name Name of the project-specific `test`
          target. If `None`, the project's `test` target will be named
          `[project_name][project_test_suffix]`.
        @param project_test_suffix Suffix to append to the project name to
          generate the project's `test` target name. Only used if
          `project_test_target_name` is `None`.
        @throws RuntimeError Thrown if the project scope already exists with the
          same name and was declared at a different location.
        @return The view for the project scope.
        """
        # Determine the project's `all` target name.
        if project_all_target_name is None:
            project_all_target_name = f"{project_name}{project_all_suffix}"

        # Determine the project's `test` target name.
        if project_test_target_name is None:
            project_test_target_name = f"{project_name}{project_test_suffix}"

        return ProjectScopeView(
            self._project,
            self._project.add_project_scope(
                project_name,
                project_languages,
                project_all_target_name,
                project_test_target_name
            )
        )
