from pymake.model.pymake_project import PyMakeProject
from pymake.visitors.hierarchical.hierarchical_state import HierarchicalState
from pymake.visitors.hierarchical.project_visitor import ProjectVisitor
from pymake.visitors.visitor import IVisitor
from pymake.visitors.visitor_set import IVisitorSet
from typing import Any

class HierarchicalVisitorSet(IVisitorSet):
    """
    Visitor set that generates CMake code in a hierarchical manner.
    """
    def __init__(self, project: PyMakeProject):
        """
        Initializes the visitor set.
        """
        ## Stores persistent state data gathered during the preprocessing phase.
        # This data is used during the visit phase and should be considered
        #   immutable during that phase.
        self._state = HierarchicalState(project)


    def get_visitor_for_node(self, node: Any) \
        -> IVisitor[Any, Any]:
        """
        Gets the visitor for the specified node.
        @param node The node to get the visitor for.
        @return The visitor for the specified node.
        """
        if isinstance(node, PyMakeProject):
            return ProjectVisitor(self._state)
        raise NotImplementedError()


    def generate_build_scripts(self) -> None:
        """
        Generates the build scripts for the project.
        """
        self._state.generate_build_scripts()
