from abc import ABC, abstractmethod
from pymake.model.targets.interface_target import InterfaceTarget

class IInterfaceTargetVisitor(ABC):
    """
    Base type for classes that generate CMake code for an interface target.
    """
    @abstractmethod
    def visit(self, target: InterfaceTarget) -> None:
        """
        Generates the CMake code for the interface target.
        @param target The interface target to generate CMake code for.
        """
        raise NotImplementedError()
