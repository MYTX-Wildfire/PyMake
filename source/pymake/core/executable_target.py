from pymake.common.target_type import ETargetType
from pymake.core.project_state import ProjectState
from pymake.core.target import Target
from pymake.generation.basic_generator import BasicGenerator

class ExecutableTarget(Target):
    """
    Represents a CMake executable target.
    """
    def __init__(self,
        project_state: ProjectState,
        target_name: str,
        caller_offset: int):
        """
        Initializes the object.
        @param project_state State information for the PyMake project that the
          target is part of.
        @param target_name Name of the target.
        @param caller_offset Number of stack frames to traverse to get to
          the stack frame of the pymake build script.
        @throws ValueError Thrown if any parameter is invalid.
        """
        super().__init__(
            project_state,
            target_name,
            ETargetType.EXECUTABLE,
            caller_offset + 1
        )

        # Add the equivalent CMake code
        build_script = project_state.get_or_add_build_script(caller_offset + 1)
        build_script.add_generator(BasicGenerator(
            f"add_executable({target_name})",
            caller_offset + 1
        ))
