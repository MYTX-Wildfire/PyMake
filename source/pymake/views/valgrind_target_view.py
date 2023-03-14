from pymake.model.targets.test.valgrind_test_target import ValgrindTestTarget
from pymake.model.project_scope import ProjectScope
from pymake.model.pymake_project import PyMakeProject
from pymake.model.target_set import TargetSet

class ValgrindTargetView:
    """
    Provides an interface for modifying a Valgrind test target.
    """
    def __init__(self,
        project: PyMakeProject,
        project_scope: ProjectScope,
        target_set: TargetSet,
        target: ValgrindTestTarget):
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
    def target(self) -> ValgrindTestTarget:
        """
        Gets the target this view is for.
        """
        return self._target
