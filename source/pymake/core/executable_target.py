from pymake.common.target_type import ETargetType
from pymake.core.project_state import ProjectState
from pymake.core.target import Target
from pymake.generation.basic_generator import BasicGenerator
from pymake.helpers.code_generator import CodeGenerator

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
            ETargetType.EXECUTABLE
        )

        # Generate the CMake code for adding the target
        generator = CodeGenerator()
        generator.append_line(f"add_executable({target_name})")

        # Add the generated CMake code
        build_script = project_state.get_or_add_build_script()
        build_script.add_generator(BasicGenerator(
            generator.code
        ))
