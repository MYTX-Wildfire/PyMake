from pymake.visitors.null.null_visitor import NullVisitor
from pymake.visitors.visitor_set import IVisitorSet
from typing import Any

class NullVisitorSet(IVisitorSet):
    """
    Visitor set that always provides null visitors.
    """
    def get_visitor_for_node(self, node: Any) \
        -> NullVisitor[Any, Any]:
        """
        Gets the visitor for the specified node.
        @param node The node to get the visitor for.
        @return The visitor for the specified node.
        """
        return NullVisitor()
