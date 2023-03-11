from pymake.model.targets.build.executable_target import ExecutableTarget
from pymake.model.targets.target import Target

class TestWrapperTarget(Target):
    """
    Represents a test target that executes an executable built by the project.
    Unlike `TestTarget`-derived types, `TestWrapperTarget`-derived types do not
      build an executable themselves.
    """
    def __init__(self,
        target_name: str,
        test_flags: int,
        sanitizer_flags: int,
        wrapped_target: ExecutableTarget):
        """
        Initializes the target.
        @param target_name The name of the target.
        @param test_flags Identifies whether the target is a test target and
          what kind of target the test target is.
        @param sanitizer_flags The sanitizers enabled for the target.
        @param wrapped_target The executable target that is wrapped by this
          target.
        """
        super().__init__(
            target_name,
            test_flags,
            sanitizer_flags
        )
        self._wrapped_target = wrapped_target


    @property
    def wrapped_target(self) -> ExecutableTarget:
        """
        Gets the executable target that is wrapped by this target.
        """
        return self._wrapped_target
