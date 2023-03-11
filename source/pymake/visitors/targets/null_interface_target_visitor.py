from pymake.model.targets.interface_target import InterfaceTarget
from pymake.visitors.targets.interface_target_visitor import IInterfaceTargetVisitor

class NullInterfaceTargetVisitor(IInterfaceTargetVisitor):
    """
    Represents a visitor that does nothing.
    """
    def visit(self, target: InterfaceTarget) -> None:
        """
        Generates the CMake code for the target.
        @param target The target to generate CMake code for.
        """
        # Do nothing
        pass
