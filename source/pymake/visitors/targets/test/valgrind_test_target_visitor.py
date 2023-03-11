from abc import ABC, abstractmethod
from pymake.model.targets.test.valgrind_test_target import ValgrindTestTarget

class IValgrindTestTargetVisitor(ABC):
    """
    Base type for classes that generate CMake code for a ValgrindTest target.
    """
    @abstractmethod
    def visit(self, target: ValgrindTestTarget) -> None:
        """
        Generates the CMake code for the ValgrindTest target.
        @param target The ValgrindTest target to generate CMake code for.
        """
        raise NotImplementedError()
