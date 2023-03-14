from pymake.common.sanitizer_flags import ESanitizerFlags
from pymake.model.targets.build.build_target import BuildTarget

class SanitizedTarget(BuildTarget):
    """
    Wraps an existing target and rebuilds it with sanitizers enabled.
    """
    def __init__(self,
        target_name: str,
        sanitizer_flags: int,
        wrapped_target: BuildTarget):
        """
        Initializes the sanitized target.
        @param target_name The name of the target.
        @param sanitizer_flags The sanitizers enabled for the target. Must have
          at least one flag enabled.
        @param wrapped_target The target to wrap. Should be a target with no
          sanitizers enabled.
        @throws RuntimeError Thrown if no sanitizer flags were set.
        @throws RuntimeError Thrown if the wrapped target has sanitizers enabled.
        """
        super().__init__(
            target_name,
            wrapped_target.target_type,
            wrapped_target.test_flags,
            sanitizer_flags
        )
        self._wrapped_target = wrapped_target

        if sanitizer_flags == ESanitizerFlags.NONE:
            raise RuntimeError("No sanitizer flags were set.")
        if wrapped_target.sanitizer_flags != ESanitizerFlags.NONE:
            raise RuntimeError("The wrapped target has sanitizers enabled.")


    @property
    def wrapped_target(self) -> BuildTarget:
        """
        Gets the target being wrapped.
        """
        return self._wrapped_target
