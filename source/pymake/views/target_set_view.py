from pymake.model.project_scope import ProjectScope
from pymake.model.pymake_project import PyMakeProject
from pymake.model.target_set import TargetSet
from typing import Optional

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
