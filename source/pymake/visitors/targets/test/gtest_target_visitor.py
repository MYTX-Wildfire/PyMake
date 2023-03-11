from abc import ABC, abstractmethod
from pymake.model.targets.test.gtest_target import GTestTarget

class IGTestTargetVisitor(ABC):
    """
    Base type for classes that generate CMake code for a GTest target.
    """
    @abstractmethod
    def visit(self, target: GTestTarget) -> None:
        """
        Generates the CMake code for the GTest target.
        @param target The GTest target to generate CMake code for.
        """
        raise NotImplementedError()
