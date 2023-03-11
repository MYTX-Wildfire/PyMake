from pymake.visitors.null.null_visitor import NullVisitor
from pymake.visitors.visitor_set import IVisitorSet
from typing import TypeVar

NodeType = TypeVar('NodeType')

class NullVisitorSet(IVisitorSet):
    """
    Visitor set that always provides null visitors.
    """
    def get_visitor_for_node(self, node: NodeType) -> NullVisitor[NodeType]:
        """
        Gets the visitor for the specified node.
        @param node The node to get the visitor for.
        @return The visitor for the specified node.
        """
        return NullVisitor()
