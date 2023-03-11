from abc import ABC, abstractmethod
from pymake.core.build_script import BuildScript
from pymake.tracing.traced import ITraced

class ITargetSet(ABC, ITraced):
    """
    Groups logically identical targets together.
    """
    @abstractmethod
    def generate_target_set(self,
        build_script: BuildScript) -> None:
        """
        Generates the CMake code for the object.
        @param build_script The build script to write the target set's CMake
          code to.
        """
        raise NotImplementedError()
