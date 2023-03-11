from abc import ABC, abstractmethod
from pymake.model.targets.target import Target
from pymake.tracing.traced import ITraced
from typing import Iterable

class ITargetSet(ABC, ITraced):
    """
    Groups logically identical targets together.
    """
    def __init__(self, name: str):
        """
        Initializes the target set.
        @param name Name of the target set.
        """
        self._name = name


    @property
    def set_name(self) -> str:
        """
        Gets the name of the target set.
        """
        return self._name


    @property
    @abstractmethod
    def targets(self) -> Iterable[Target]:
        """
        Gets the targets in this target set.
        """
        raise NotImplementedError()
