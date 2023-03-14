from pymake.model.targets.test.drd_test_target import DrdTestTarget
from pymake.visitors.hierarchical.hierarchical_state import HierarchicalState
from pymake.visitors.hierarchical.valgrind_target_visitor \
    import ValgrindTargetVisitor

class DrdTargetVisitor(ValgrindTargetVisitor[DrdTestTarget]):
    """
    Visitor that generates CMake code for a DRD test target.
    """
    def __init__(self,
        target: DrdTestTarget,
        state: HierarchicalState):
        """
        Initializes the test wrapper target visitor.
        @param target The test wrapper target to generate code for.
        @param command Command to use to invoke the test.
        @param state Stores persistent state data gathered during the
            preprocessing phase. This data is used during the visit phase and
            should be considered immutable during that phase.
        """
        # TODO: Generate the command to invoke DRD from a constructor parameter
        super().__init__(
            target,
            [
                "--tool=drd",
                "--fair-sched=yes",
                "--error-exitcode=1",
                str(state.get_target_build_path(target.wrapped_target))
            ],
            state
        )
