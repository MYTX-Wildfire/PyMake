from abc import ABC, abstractmethod
from pymake.model.targets.test.test_wrapper_target import TestWrapperTarget

class ITestWrapperTargetVisitor(ABC):
    """
    Base type for classes that generate CMake code for a TestWrapper target.
    """
    @abstractmethod
    def visit(self, target: TestWrapperTarget) -> None:
        """
        Generates the CMake code for the TestWrapper target.
        @param target The TestWrapper target to generate CMake code for.
        """
        raise NotImplementedError()
