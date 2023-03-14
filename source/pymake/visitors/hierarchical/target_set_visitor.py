from pymake.model.target_set import TargetSet
from pymake.model.targets.target import Target
from pymake.visitors.hierarchical.hierarchical_state import HierarchicalState
from pymake.visitors.visitor import IVisitor
from typing import Iterable, List, Set

class TargetSetVisitor(IVisitor[TargetSet]):
    """
    Visitor that generates CMake code for a target set.
    """
    def __init__(self, state: HierarchicalState):
        """
        Initializes the visitor.
        @param state Stores persistent state data gathered during the
            preprocessing phase. This data is used during the visit phase and
            should be considered immutable during that phase.
        """
        self._state = state


    def preprocess(self, node: TargetSet) -> None:
        """
        Pre-processes the model object.
        @param node The model object to preprocess.
        """
        # Nothing to do
        pass


    def visit(self, node: TargetSet) -> None:
        """
        Visits the specified target set.
        @param node The target set to visit.
        """
        generator = self._state.get_build_script_for_node(node).generator

        # Get a list of all targets in the target set, sorted by the order
        #   that the targets should be added via `add_subdirectory()` calls
        targets: List[Target] = []

        # Keep track of the names of all targets that have been added to avoid
        #   adding the same target twice
        target_names: Set[str] = set()

        def add(target: Target | Iterable[Target]) -> None:
            """
            Adds the target to the targets list if it hasn't already been added.
            """
            if isinstance(target, Target):
                target = [target]

            for t in target:
                if t.target_name not in target_names:
                    targets.append(t)
                    target_names.add(t.target_name)

        # Start with set's common target since other many other targets depend
        #   on it
        add(node.common_target)

        # Add imported targets next since they're likely to not have
        #   dependencies within the target set
        add(node.imported_targets)

        # Add library targets before executable targets since executable
        #   targets may depend on library targets
        add(node.library_targets)

        # Add non-sanitized, non-test executables next since they're likely to
        #   only depend on libraries in the set or imported targets
        add([t for t in node.executable_targets if not t.is_sanitized])

        # Add any sanitized targets not already added
        add(node.sanitized_targets)

        # Add test targets last since they're likely to depend on other
        #   targets in the set
        add(node.test_targets)

        # Add each target
        for target in targets:
            with generator.open_method_block("add_subdirectory") as b:
                b.add_arguments(target.target_name)
