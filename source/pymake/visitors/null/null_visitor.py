from pymake.visitors.visitor import IVisitor
from typing import Generic, TypeVar

NodeType = TypeVar('NodeType')
ChildNodeType = TypeVar('ChildNodeType')

class NullVisitor(
    IVisitor[NodeType, ChildNodeType],
    Generic[NodeType, ChildNodeType]):
    """
    Base type for classes that visit a model object and generate CMake code.
    """
    def preprocess(self, node: NodeType) -> None:
        """
        Pre-processes the model object.
        @param node The model object to preprocess.
        """
        # Do nothing
        pass


    def visit(self, node: NodeType) -> None:
        """
        Visits the model object.
        @pre All nodes will have been passed to a visitor's preprocess method
          before any node may be passed to a visitor's visit method.
        @param node The model object to visit.
        """
        # Do nothing
        pass
