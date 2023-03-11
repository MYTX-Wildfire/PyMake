from abc import ABC, abstractmethod
from pymake.model.targets.test.drd_test_target import DrdTestTarget

class IDrdTestTargetVisitor(ABC):
    """
    Base type for classes that generate CMake code for a DrdTest target.
    """
    @abstractmethod
    def visit(self, target: DrdTestTarget) -> None:
        """
        Generates the CMake code for the DrdTest target.
        @param target The DrdTest target to generate CMake code for.
        """
        raise NotImplementedError()
