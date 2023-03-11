from pymake.common.sanitizer_flags import ESanitizerFlags
from pymake.common.target_type import ETargetType
from pymake.common.test_flags import ETestFlags
from pymake.generators.build_script import BuildScript
from pymake.model.targets.target import Target

class InterfaceTarget(Target):
    """
    Represents an interface target.
    """
    def __init__(self,
        target_name: str):
        """
        Initializes the target.
        @param target_name The name of the target.
        """
        super().__init__(
            target_name,
            ETargetType.INTERFACE,
            # An interface target can never be a test target
            ETestFlags.NONE,
            # An interface target cannot be a sanitizer target
            ESanitizerFlags.NONE
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
