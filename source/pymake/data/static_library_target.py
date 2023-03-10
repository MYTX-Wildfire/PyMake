from pymake.common.target_type import ETargetType
from pymake.data.library_target import LibraryTarget

class StaticLibraryTarget(LibraryTarget):
    """
    Represents a static library target.
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
            ETargetType.STATIC,
            sanitizer_flags
        )
