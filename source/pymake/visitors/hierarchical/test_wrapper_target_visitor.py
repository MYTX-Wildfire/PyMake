from pymake.model.targets.test.test_wrapper_target import TestWrapperTarget
from pymake.visitors.hierarchical.hierarchical_state import HierarchicalState
from pymake.visitors.visitor import IVisitor
from typing import Generic, Iterable, TypeVar

TargetType = TypeVar('TargetType', bound=TestWrapperTarget)

class TestWrapperTargetVisitor(IVisitor[TargetType], Generic[TargetType]):
    """
    Base type for visitors that generate test wrapper targets.
    """
    def __init__(self,
        target: TargetType,
        command: str | Iterable[str],
        state: HierarchicalState):
        """
        Initializes the test wrapper target visitor.
        @param target The test wrapper target to generate code for.
        @param command Command to use to invoke the test.
        @param state Stores persistent state data gathered during the
            preprocessing phase. This data is used during the visit phase and
            should be considered immutable during that phase.
        """
        self._target = target
        self._command = [command] if isinstance(command, str) else list(command)
        self._state = state


    def preprocess(self, node: TargetType) -> None:
        """
        Pre-processes the model object.
        @param node The model object to preprocess.
        """
        # Do nothing
        pass


    def visit(self, node: TargetType) -> None:
        """
        Visits the model object.
        @param node The model object to visit.
        """
        generator = self._state.get_build_script_for_node(node).generator

        # Generate the test declaration
        with generator.open_method_block("add_test") as b:
            b.add_keyword_arguments(
                "NAME",
                self._target.target_name
            )
            b.add_keyword_arguments(
                "COMMAND",
                *self._command
            )

        # TODO: Add the target to the target set's test target and to the
        #   project's test target.
