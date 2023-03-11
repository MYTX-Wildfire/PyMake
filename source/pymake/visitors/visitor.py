from abc import ABC, abstractmethod
from typing import Generic, TypeVar

NodeType = TypeVar('NodeType')

class IVisitor(ABC, Generic[NodeType]):
    """
    Base type for classes that visit a model object and generate CMake code.
    """
    @abstractmethod
    def preprocess(self, node: NodeType) -> None:
        """
        Pre-processes the model object.
        @param node The model object to preprocess.
        """
        raise NotImplementedError()


    @abstractmethod
    def visit(self, node: NodeType) -> None:
        """
        Visits the model object.
        @param node The model object to visit.
        """
        raise NotImplementedError()
