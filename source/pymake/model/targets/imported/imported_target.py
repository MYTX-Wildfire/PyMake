from pymake.common.target_type import ETargetType
from pymake.common.test_flags import ETestFlags
from pymake.model.targets.target import Target

class ImportedTarget(Target):
    """
    Represents a target that is built externally and imported into the project.
    """
    def __init__(self,
        target_name: str,
        target_type: ETargetType,
        sanitizer_flags: int):
        """
        Initializes the target.
        @param target_name The name of the target.
        @param sanitizer_flags Sanitizers that were enabled when the target was
          built.
        """
        super().__init__(
            target_name,
            # Imported targets should never be test targets.
            ETestFlags.NONE,
            sanitizer_flags
        )
        self._target_type = target_type


    @property
    def target_type(self) -> ETargetType:
        """
        Gets the type of the target.
        """
        return self._target_type
