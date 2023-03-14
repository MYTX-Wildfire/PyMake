from pathlib import Path
from pymake.model.targets.build.sanitized_target import SanitizedTarget
from pymake.model.project_scope import ProjectScope
from pymake.model.pymake_project import PyMakeProject
from pymake.model.target_set import TargetSet

class SanitizedTargetView:
    """
    Provides an interface for modifying a sanitized target.
    """
    def __init__(self,
        project: PyMakeProject,
        project_scope: ProjectScope,
        target_set: TargetSet,
        target: SanitizedTarget):
        """
        Initializes the target set view.
        @param project The project that the target's project scope belongs to.
        @param project_scope The project scope that the target belongs to.
        @param target_set The target set that the target belongs to.
        @param target The target to provide a view for.
        """
        self._project = project
        self._project_scope = project_scope
        self._target_set = target_set
        self._target = target


    @property
    def target_name(self) -> str:
        """
        Gets the name of the target.
        """
        return self._target.target_name


    @property
    def target(self) -> SanitizedTarget:
        """
        Gets the target this view is for.
        """
        return self._target


    def install(self, install_path: str | Path | None = None) -> None:
        """
        Installs the target.
        @param install_path The path to install the target to. If this is a
          relative path, it will be interpreted relative to the install prefix.
          If this is `None`, the target will be installed to CMake's default
          install path for the target type.
        """
        self._target.properties.install(install_path)
