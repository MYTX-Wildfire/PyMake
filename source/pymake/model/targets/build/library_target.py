from pymake.common.target_type import ETargetType
from pymake.common.test_flags import ETestFlags
from pymake.core.build_script import BuildScript
from pymake.model.targets.target import Target

class LibraryTarget(Target):
    """
    Represents a static or shared library target.
    """
    def __init__(self,
        target_name: str,
        target_type: ETargetType,
        sanitizer_flags: int):
        """
        Initializes the target.
        @param target_name The name of the target.
        @param target_type The type of the target. Must be either
          `ETargetType.STATIC` or `ETargetType.SHARED`.
        @param sanitizer_flags The sanitizers enabled for the target.
        """
        assert target_type in (ETargetType.STATIC, ETargetType.SHARED)
        super().__init__(
            target_name,
            target_type,
            # A library target can never be a test target
            ETestFlags.NONE,
            sanitizer_flags
        )


    def _generate_declaration(self,
        build_script: BuildScript) -> None:
        """
        Generates the CMake code for the declaration of the target.
        @param build_script Build script to write the target to.
        """
        with build_script.generator.open_method_block("add_library") as b:
            b.add_arguments(
                self.target_name,
                self._target_type.value
            )
