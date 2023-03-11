from pymake.model.pymake_project import PyMakeProject
from pymake.visitors.hierarchical.hierarchical_state import HierarchicalState
from pymake.visitors.visitor import IVisitor

class ProjectVisitor(IVisitor[PyMakeProject]):
    """
    Visitor that generates top-level CMake code for a project.
    """
    def __init__(self, state: HierarchicalState):
        """
        Initializes the visitor.
        @param state Stores persistent state data gathered during the
            preprocessing phase. This data is used during the visit phase and
            should be considered immutable during that phase.
        """
        self._state = state


    def preprocess(self, node: PyMakeProject) -> None:
        """
        Pre-processes the model object.
        @param node The model object to preprocess.
        """
        # Nothing to do
        pass


    def visit(self, node: PyMakeProject) -> None:
        """
        Visits the model object.
        @param node The model object to visit.
        """
        generator = self._state.get_build_script_for_node(node).generator

        # Generate the cmake_minimum_required() call
        with generator.open_method_block("cmake_minimum_required") as b:
            b.add_keyword_arguments("VERSION", node.cmake_version.value)

        # Generate add_subdirectory() calls for each project scope
        for scope in node.project_scopes:
            with generator.open_method_block("add_subdirectory") as b:
                b.add_arguments(scope.project_name)
