from pymake.common.sanitizer_flags import ESanitizerFlags
from pymake.common.test_flags import ETestFlags
from pymake.model.targets.target import Target

class CustomTarget(Target):
    """
    Represents a custom command target within a PyMake project.
    """
    def __init__(self,
        target_name: str):
        """
        Initializes the target.
        @param target_name The name of the target.
        """
        super().__init__(
            target_name,
            # Custom targets are never test targets
            ETestFlags.NONE,
            # Custom targets are never sanitized
            ESanitizerFlags.NONE
        )
