from abc import ABC, abstractmethod
from pymake.model.targets.test.memcheck_test_target import MemcheckTestTarget

class IMemcheckTestTargetVisitor(ABC):
    """
    Base type for classes that generate CMake code for a MemcheckTest target.
    """
    @abstractmethod
    def visit(self, target: MemcheckTestTarget) -> None:
        """
        Generates the CMake code for the MemcheckTest target.
        @param target The MemcheckTest target to generate CMake code for.
        """
        raise NotImplementedError()
