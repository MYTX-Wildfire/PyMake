from pymake.generators.cmake_generator import CMakeGenerator
from pymake.model.targets.build.interface_target import InterfaceTarget
from pymake.tracing.traced import Traced
from pymake.visitors.hierarchical.hierarchical_state import HierarchicalState
from pymake.visitors.hierarchical.target_visitor import ITargetVisitor

class InterfaceTargetVisitor(ITargetVisitor[InterfaceTarget]):
    """
    Visitor that generates CMake code for an interface target.
    """
    def __init__(self, state: HierarchicalState):
        """
        Initializes the visitor.
        @param state Stores persistent state data gathered during the
            preprocessing phase. This data is used during the visit phase and
            should be considered immutable during that phase.
        """
        self._state = state


    def preprocess(self, node: InterfaceTarget) -> None:
        """
        Pre-processes the model object.
        @param node The model object to preprocess.
        """
        # Nothing to do
        pass


    def visit(self, node: InterfaceTarget) -> None:
        """
        Visits the model object.
        @param node The model object to visit.
        """
        generator = self._state.get_build_script_for_node(node).generator
        self._generate(node, generator)


    def _generate_target_declaration(self,
        target: InterfaceTarget,
        generator: CMakeGenerator) -> None:
        """
        Generates the CMake code for the declaration of the target.
        @param target The target to generate CMake code for.
        @param generator The CMake generator to add code to.
        """
        with generator.open_method_block("add_library") as b:
            b.add_arguments(
                Traced(target.target_name, target.origin)
            )
            b.add_arguments("INTERFACE")
