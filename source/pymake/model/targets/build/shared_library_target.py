from pymake.common.target_type import ETargetType
from pymake.model.targets.build.library_target import LibraryTarget

class SharedLibraryTarget(LibraryTarget):
    """
    Represents a shared library target.
    """
    def __init__(self,
        target_name: str,
        sanitizer_flags: int):
        """
        Initializes the target.
        @param target_name The name of the target.
        @param sanitizer_flags The sanitizers enabled for the target.
        """
        super().__init__(
            target_name,
            ETargetType.SHARED,
            sanitizer_flags
        )
