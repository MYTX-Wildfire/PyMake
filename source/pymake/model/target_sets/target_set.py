from abc import ABC, abstractmethod
from pymake.model.targets.target import Target
from pymake.tracing.traced import ITraced
from typing import Iterable

class ITargetSet(ABC, ITraced):
    """
    Groups logically identical targets together.
    """
    @property
    @abstractmethod
    def targets(self) -> Iterable[Target]:
        """
        Gets the targets in this target set.
        """
        raise NotImplementedError()
