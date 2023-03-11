from abc import ABC, abstractmethod
from pymake.model.pymake_project import PyMakeProject

class IProjectCrawler(ABC):
    """
    Class that crawls the project tree and invokes visitors on each node.
    """
    @abstractmethod
    def crawl(self, project: PyMakeProject) -> None:
        """
        Crawls the project tree and invokes visitors on each node.
        @param project The project to crawl.
        """
        raise NotImplementedError()
