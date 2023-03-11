from pymake.model.pymake_project import PyMakeProject
from pymake.visitors.target_set.null_executable_set_visitor import NullExecutableSetVisitor
from pymake.visitors.target_set.null_library_set_visitor import NullLibrarySetVisitor
from pymake.visitors.null.null_project_visitor import NullProjectVisitor
from pymake.visitors.null.null_project_scope_visitor import NullProjectScopeVisitor
from pymake.visitors.target_set.executable_set_visitor import IExecutableSetVisitor
from pymake.visitors.target_set.library_set_visitor import ILibrarySetVisitor
from pymake.visitors.project_crawler import IProjectCrawler
from pymake.visitors.project_scope_visitor import IProjectScopeVisitor
from pymake.visitors.project_visitor import IProjectVisitor

class BreadthFirstCrawler(IProjectCrawler):
    """
    Class that crawls the project tree and invokes visitors on each node.
    This crawler operates in a breadth-first manner by visiting the pymake
      project node first, followed by all project scopes, followed by all
      target sets, and finally all targets.
    """
    def __init__(self,
        project_visitor: IProjectVisitor = NullProjectVisitor(),
        project_scope_visitor: IProjectScopeVisitor = NullProjectScopeVisitor(),
        executable_set_visitor: IExecutableSetVisitor = NullExecutableSetVisitor(),
        library_set_visitor: ILibrarySetVisitor = NullLibrarySetVisitor()):
        """
        Initializes the crawler.
        @param project_visitor The visitor to invoke on the project.
        @param project_scope_visitor The visitor to invoke on each project scope.
        """
        self._project_visitor = project_visitor
        self._project_scope_visitor = project_scope_visitor


    def crawl(self, project: PyMakeProject) -> None:
        """
        Crawls the project tree and invokes visitors on each node.
        @param project The project to crawl.
        """
        raise NotImplementedError()
