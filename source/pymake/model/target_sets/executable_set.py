from pymake.core.build_script import BuildScript
from pymake.model.target_sets.target_set import ITargetSet

class ExecutableSet(ITargetSet):
    """
    Target set whose primary target is an executable.
    """
    def generate_target_set(self,
        build_script: BuildScript) -> None:
        """
        Generates the CMake code for the object.
        @param build_script The build script to write the target set's CMake
          code to.
        """
        raise NotImplementedError()
