from abc import ABC, abstractmethod
from pymake.model.targets.test.test_target import TestTarget

class ITestTargetVisitor(ABC):
    """
    Base type for classes that generate CMake code for a Test target.
    """
    @abstractmethod
    def visit(self, target: TestTarget) -> None:
        """
        Generates the CMake code for the Test target.
        @param target The Test target to generate CMake code for.
        """
        raise NotImplementedError()
