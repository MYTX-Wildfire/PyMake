from abc import ABC, abstractmethod
from pymake.visitors.visitor import IVisitor
from typing import Any

class IVisitorSet(ABC):
    """
    Base type for classes that contain a set of visitors.
    """
    @abstractmethod
    def get_visitor_for_node(self, node: Any) -> IVisitor[Any]:
        """
        Gets the visitor for the specified node.
        @param node The node to get the visitor for.
        @return The visitor for the specified node.
        """
        raise NotImplementedError()


    @abstractmethod
    def generate_build_scripts(self) -> None:
        """
        Generates the build scripts for the project.
        """
        raise NotImplementedError()
