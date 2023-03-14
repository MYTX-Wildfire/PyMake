from pymake.model.targets.test.valgrind_test_target import ValgrindTestTarget
from pymake.visitors.hierarchical.hierarchical_state import HierarchicalState
from pymake.visitors.hierarchical.test_wrapper_target_visitor \
    import TestWrapperTargetVisitor
from typing import Iterable, TypeVar

ValgrindTargetType = TypeVar('ValgrindTargetType', bound=ValgrindTestTarget)

class ValgrindTargetVisitor(TestWrapperTargetVisitor[ValgrindTargetType]):
    """
    Visitor that generates CMake code for a Valgrind test target.
    """
    def __init__(self,
        target: ValgrindTargetType,
        args: str | Iterable[str],
        state: HierarchicalState):
        """
        Initializes the test wrapper target visitor.
        @param target The test wrapper target to generate code for.
        @param args Arguments to pass to Valgrind.
        @param state Stores persistent state data gathered during the
            preprocessing phase. This data is used during the visit phase and
            should be considered immutable during that phase.
        """
        if isinstance(args, str):
            args = [args]

        super().__init__(
            target,
            [
                "valgrind",
                *args
            ],
            state
        )
