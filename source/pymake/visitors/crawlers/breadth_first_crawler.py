from pymake.model.target_set import TargetSet
from pymake.model.targets.target import Target
from pymake.model.pymake_project import PyMakeProject
from pymake.visitors.crawlers.project_crawler import IProjectCrawler
from pymake.visitors.visitor import IVisitor
from pymake.visitors.visitor_set import IVisitorSet
from typing import Any, Callable, List

class BreadthFirstCrawler(IProjectCrawler):
    """
    Class that crawls the project tree and invokes visitors on each node.
    This crawler operates in a breadth-first manner by visiting the pymake
      project node first, followed by all project scopes, followed by all
      target sets, and finally all targets.
    """
    def crawl(self,
        project: PyMakeProject,
        visitor_set: IVisitorSet) -> None:
        """
        Crawls the project tree and invokes visitors on each node.
        @param project The project to crawl.
        @param visitor_set The visitor set to use to generate build scripts.
        """
        # Run the preprocessing phase
        self._crawl(
            visitor_set,
            project,
            lambda visitor, node: visitor.preprocess(node)
        )

        # Run the visit phase
        self._crawl(
            visitor_set,
            project,
            lambda visitor, node: visitor.visit(node)
        )

        # Finish up
        visitor_set.generate_build_scripts()


    def _crawl(self,
        visitors: IVisitorSet,
        project: PyMakeProject,
        visit: Callable[[IVisitor[Any], Any], None]) -> None:
        """
        Crawls the project tree and invokes visitors on each node.
        @param visitors The visitor set to use when crawling the project tree.
        @param project The project to crawl.
        @param visit Functor to use to invoke the correct visitor method on the
          node.
        """
        # Process the project node first
        project_visitor = visitors.get_visitor_for_node(project)
        visit(project_visitor, project)

        # Process each project scope
        target_sets: List[TargetSet] = []
        for scope in project.project_scopes:
            scope_visitor = visitors.get_visitor_for_node(scope)
            visit(scope_visitor, scope)
            target_sets.extend(scope.target_sets)

        # Process each target set
        targets: List[Target] = []
        for target_set in target_sets:
            target_set_visitor = visitors.get_visitor_for_node(target_set)
            visit(target_set_visitor, target_set)
            targets.extend(target_set.targets)

        # Process each target
        for target in targets:
            target_visitor = visitors.get_visitor_for_node(target)
            visit(target_visitor, target)
