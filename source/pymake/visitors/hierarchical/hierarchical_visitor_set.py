from pymake.model.pymake_project import PyMakeProject
from pymake.model.project_scope import ProjectScope
from pymake.model.target_set import TargetSet
from pymake.model.targets.build.executable_target import ExecutableTarget
from pymake.model.targets.build.library_target import LibraryTarget
from pymake.model.targets.build.interface_target import InterfaceTarget
from pymake.visitors.hierarchical.executable_target_visitor import ExecutableTargetVisitor
from pymake.visitors.hierarchical.library_target_visitor import LibraryTargetVisitor
from pymake.visitors.hierarchical.interface_target_visitor import InterfaceTargetVisitor
from pymake.visitors.hierarchical.hierarchical_state import HierarchicalState
from pymake.visitors.hierarchical.project_visitor import ProjectVisitor
from pymake.visitors.hierarchical.project_scope_visitor import ProjectScopeVisitor
from pymake.visitors.hierarchical.target_set_visitor import TargetSetVisitor
from pymake.visitors.visitor import IVisitor
from pymake.visitors.visitor_set import IVisitorSet
from typing import TypeVar

NodeType = TypeVar('NodeType')

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


    def get_visitor_for_node(self, node: NodeType) -> IVisitor[NodeType]:
        """
        Gets the visitor for the specified node.
        @param node The node to get the visitor for.
        @return The visitor for the specified node.
        """
        # The `type: ignore` lines are needed to stop PyRight from complaining
        #   that the visitors are not compatible with `IVisitor[NodeType]`.
        if isinstance(node, PyMakeProject):
            return ProjectVisitor(self._state) # type: ignore
        elif isinstance(node, ProjectScope):
            return ProjectScopeVisitor(self._state) # type: ignore
        elif isinstance(node, TargetSet):
            return TargetSetVisitor(self._state) # type: ignore
        elif isinstance(node, ExecutableTarget):
            return ExecutableTargetVisitor(self._state) # type: ignore
        elif isinstance(node, LibraryTarget):
            return LibraryTargetVisitor(self._state) # type: ignore
        elif isinstance(node, InterfaceTarget):
            return InterfaceTargetVisitor(self._state) # type: ignore
        raise NotImplementedError()


    def generate_build_scripts(self) -> None:
        """
        Generates the build scripts for the project.
        """
        self._state.generate_build_scripts()
