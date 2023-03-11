from pymake.model.target_sets.executable_set import ExecutableSet
from pymake.model.target_sets.library_set import LibrarySet
from pymake.model.target_sets.target_set import ITargetSet
from pymake.model.targets.target import Target
from pymake.model.targets.build.build_target import BuildTarget
from pymake.model.targets.build.executable_target import ExecutableTarget
from pymake.model.targets.build.library_target import LibraryTarget
from pymake.model.targets.build.shared_library_target import SharedLibraryTarget
from pymake.model.targets.build.static_library_target import StaticLibraryTarget
from pymake.model.targets.docs.documentation_target import DocumentationTarget
from pymake.model.targets.docs.doxygen_target import DoxygenTarget
from pymake.model.targets.imported.external_library_target import ExternalLibraryTarget
from pymake.model.targets.imported.imported_target import ImportedTarget
from pymake.model.targets.test.drd_test_target import DrdTestTarget
from pymake.model.targets.test.gtest_target import GTestTarget
from pymake.model.targets.test.helgrind_test_target import HelgrindTestTarget
from pymake.model.targets.test.memcheck_test_target import MemcheckTestTarget
from pymake.model.targets.test.test_target import TestTarget
from pymake.model.targets.test.test_wrapper_target import TestWrapperTarget
from pymake.model.targets.test.valgrind_test_target import ValgrindTestTarget
from pymake.model.project_scope import ProjectScope
from pymake.model.pymake_project import PyMakeProject
from pymake.visitors.crawlers.project_crawler import IProjectCrawler
from pymake.visitors.visitor_set import VisitorSet
from typing import List

class BreadthFirstCrawler(IProjectCrawler):
    """
    Class that crawls the project tree and invokes visitors on each node.
    This crawler operates in a breadth-first manner by visiting the pymake
      project node first, followed by all project scopes, followed by all
      target sets, and finally all targets.
    """
    def __init__(self,
        visitors: VisitorSet) -> None:
        """
        Initializes the crawler.
        @param visitors The visitors to invoke on each node.
        """
        self._visitors = visitors


    def crawl(self, project: PyMakeProject) -> None:
        """
        Crawls the project tree and invokes visitors on each node.
        @param project The project to crawl.
        """
        # Visit the project
        self._visitors.project_visitor.visit(project)

        # Visit the project scopes
        target_sets: List[ITargetSet] = []
        for project_scope in project.project_scopes:
            target_sets.extend(self._visit_project_scope(project_scope))

        # Visit the target sets
        targets: List[Target] = []
        for target_set in target_sets:
            targets.extend(self._visit_target_set(target_set))


    def _visit_project_scope(self,
        project_scope: ProjectScope) -> List[ITargetSet]:
        """
        Visits the project scope.
        @param project_scope The project scope to visit.
        @returns The target sets in the project scope.
        """
        # Visit the project scope
        self._visitors.project_scope_visitor.visit(project_scope)

        # Return all target sets
        return list(project_scope.target_sets)


    def _visit_target_set(self,
        target_set: ITargetSet) -> List[Target]:
        """
        Visits the target set.
        @param target_set The target set to visit.
        @returns The targets in the target set.
        """
        # Visit the target set
        if isinstance(target_set, ExecutableSet):
            self._visitors.executable_set_visitor.visit(target_set)
        elif isinstance(target_set, LibrarySet):
            self._visitors.library_set_visitor.visit(target_set)
        else:
            assert False, f"Unknown target set type: {type(target_set)}"

        return list(target_set.targets)


    def _visit_target(self,
        target: Target) -> None:
        """
        Visits the target.
        @param target The target to visit.
        """
        # Visit the target
        # Start with more specific targets, then move to more general targets
        if isinstance(target, GTestTarget):
            self._visitors.gtest_target_visitor.visit(target)
        elif isinstance(target, DrdTestTarget):
            self._visitors.drd_test_target_visitor.visit(target)
        elif isinstance(target, HelgrindTestTarget):
            self._visitors.helgrind_test_target_visitor.visit(target)
        elif isinstance(target, MemcheckTestTarget):
            self._visitors.memcheck_test_target_visitor.visit(target)
        elif isinstance(target, ValgrindTestTarget):
            self._visitors.valgrind_test_target_visitor.visit(target)
        elif isinstance(target, TestWrapperTarget):
            self._visitors.test_wrapper_target_visitor.visit(target)
        elif isinstance(target, TestTarget):
            self._visitors.test_target_visitor.visit(target)
        elif isinstance(target, ExecutableTarget):
            self._visitors.executable_target_visitor.visit(target)
        elif isinstance(target, SharedLibraryTarget):
            self._visitors.shared_library_target_visitor.visit(target)
        elif isinstance(target, StaticLibraryTarget):
            self._visitors.static_library_target_visitor.visit(target)
        elif isinstance(target, LibraryTarget):
            self._visitors.library_target_visitor.visit(target)
        elif isinstance(target, DoxygenTarget):
            self._visitors.doxygen_target_visitor.visit(target)
        elif isinstance(target, DocumentationTarget):
            self._visitors.documentation_target_visitor.visit(target)
        elif isinstance(target, ExternalLibraryTarget):
            self._visitors.external_library_target_visitor.visit(target)
        elif isinstance(target, ImportedTarget):
            self._visitors.imported_target_visitor.visit(target)
        elif isinstance(target, BuildTarget):
            self._visitors.build_target_visitor.visit(target)
        else:
            self._visitors.target_visitor.visit(target)
