from abc import ABC, abstractmethod
from pymake.model.pymake_project import PyMakeProject
from pymake.visitors.visitor_set import IVisitorSet

class IProjectCrawler(ABC):
    """
    Class that crawls the project tree and invokes visitors on each node.
    """
    @abstractmethod
    def crawl(self,
        project: PyMakeProject,
        visitor_set: IVisitorSet) -> None:
        """
        Crawls the project tree and invokes visitors on each node.
        @param project The project to crawl.
        @param visitor_set The visitor set to use to generate build scripts.
        """
        raise NotImplementedError()
