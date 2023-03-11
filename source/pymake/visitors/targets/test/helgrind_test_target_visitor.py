from abc import ABC, abstractmethod
from pymake.model.targets.test.helgrind_test_target import HelgrindTestTarget

class IHelgrindTestTargetVisitor(ABC):
    """
    Base type for classes that generate CMake code for a HelgrindTest target.
    """
    @abstractmethod
    def visit(self, target: HelgrindTestTarget) -> None:
        """
        Generates the CMake code for the HelgrindTest target.
        @param target The HelgrindTest target to generate CMake code for.
        """
        raise NotImplementedError()
