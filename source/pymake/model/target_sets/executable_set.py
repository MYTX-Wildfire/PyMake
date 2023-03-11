from pymake.model.target_sets.target_set import ITargetSet
from pymake.model.targets.target import Target
from typing import Iterable

class ExecutableSet(ITargetSet):
    """
    Target set whose primary target is an executable.
    """
    @property
    def targets(self) -> Iterable[Target]:
        """
        Gets the targets in this target set.
        """
        raise NotImplementedError()
