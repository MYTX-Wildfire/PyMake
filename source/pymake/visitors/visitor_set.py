from pymake.visitors.null_project_scope_visitor import NullProjectScopeVisitor
from pymake.visitors.null_project_visitor import NullProjectVisitor
from pymake.visitors.project_scope_visitor import IProjectScopeVisitor
from pymake.visitors.project_visitor import IProjectVisitor
from pymake.visitors.targets.build.build_target_visitor import IBuildTargetVisitor
from pymake.visitors.targets.build.executable_target_visitor import IExecutableTargetVisitor
from pymake.visitors.targets.build.library_target_visitor import ILibraryTargetVisitor
from pymake.visitors.targets.build.null_build_target_visitor import NullBuildTargetVisitor
from pymake.visitors.targets.build.null_executable_target_visitor import NullExecutableTargetVisitor
from pymake.visitors.targets.build.null_library_target_visitor import NullLibraryTargetVisitor
from pymake.visitors.targets.build.null_shared_library_target_visitor import NullSharedLibraryTargetVisitor
from pymake.visitors.targets.build.null_static_library_target_visitor import NullStaticLibraryTargetVisitor
from pymake.visitors.targets.build.shared_library_target_visitor import ISharedLibraryTargetVisitor
from pymake.visitors.targets.build.static_library_target_visitor import IStaticLibraryTargetVisitor
from pymake.visitors.targets.docs.documentation_target_visitor import IDocumentationTargetVisitor
from pymake.visitors.targets.docs.doxygen_target_visitor import IDoxygenTargetVisitor
from pymake.visitors.targets.docs.null_documentation_target_visitor import NullDocumentationTargetVisitor
from pymake.visitors.targets.docs.null_doxygen_target_visitor import NullDoxygenTargetVisitor
from pymake.visitors.targets.imported.external_library_target_visitor import IExternalLibraryTargetVisitor
from pymake.visitors.targets.imported.imported_target_visitor import IImportedTargetVisitor
from pymake.visitors.targets.imported.null_external_library_target_visitor import NullExternalLibraryTargetVisitor
from pymake.visitors.targets.imported.null_imported_target_visitor import NullImportedTargetVisitor
from pymake.visitors.targets.test.drd_test_target_visitor import IDrdTestTargetVisitor
from pymake.visitors.targets.test.gtest_target_visitor import IGTestTargetVisitor
from pymake.visitors.targets.test.helgrind_test_target_visitor import IHelgrindTestTargetVisitor
from pymake.visitors.targets.test.memcheck_test_target_visitor import IMemcheckTestTargetVisitor
from pymake.visitors.targets.test.null_drd_test_target_visitor import NullDrdTestTargetVisitor
from pymake.visitors.targets.test.null_gtest_target_visitor import NullGTestTargetVisitor
from pymake.visitors.targets.test.null_helgrind_test_target_visitor import NullHelgrindTestTargetVisitor
from pymake.visitors.targets.test.null_memcheck_test_target_visitor import NullMemcheckTestTargetVisitor
from pymake.visitors.targets.test.null_test_target_visitor import NullTestTargetVisitor
from pymake.visitors.targets.test.null_test_wrapper_target_visitor import NullTestWrapperTargetVisitor
from pymake.visitors.targets.test.null_valgrind_test_target_visitor import NullValgrindTestTargetVisitor
from pymake.visitors.targets.test.test_target_visitor import ITestTargetVisitor
from pymake.visitors.targets.test.test_wrapper_target_visitor import ITestWrapperTargetVisitor
from pymake.visitors.targets.test.valgrind_test_target_visitor import IValgrindTestTargetVisitor

class VisitorSet:
    """
    Represents a set of visitors that may be applied by a crawler.
    """
    def __init__(self,
        project_visitor: IProjectVisitor = NullProjectVisitor(),
        project_scope_visitor: IProjectScopeVisitor = NullProjectScopeVisitor(),
        build_target_visitor: IBuildTargetVisitor = NullBuildTargetVisitor(),
        executable_target_visitor: IExecutableTargetVisitor = NullExecutableTargetVisitor(),
        library_target_visitor: ILibraryTargetVisitor = NullLibraryTargetVisitor(),
        static_library_target_visitor: IStaticLibraryTargetVisitor = NullStaticLibraryTargetVisitor(),
        shared_library_target_visitor: ISharedLibraryTargetVisitor = NullSharedLibraryTargetVisitor(),
        documentation_target_visitor: IDocumentationTargetVisitor = NullDocumentationTargetVisitor(),
        doxygen_target_visitor: IDoxygenTargetVisitor = NullDoxygenTargetVisitor(),
        imported_target_visitor: IImportedTargetVisitor = NullImportedTargetVisitor(),
        external_library_target_visitor: IExternalLibraryTargetVisitor = NullExternalLibraryTargetVisitor(),
        test_target_visitor: ITestTargetVisitor = NullTestTargetVisitor(),
        gtest_target_visitor: IGTestTargetVisitor = NullGTestTargetVisitor(),
        test_wrapper_target_visitor: ITestWrapperTargetVisitor = NullTestWrapperTargetVisitor(),
        valgrind_test_target_visitor: IValgrindTestTargetVisitor = NullValgrindTestTargetVisitor(),
        drd_test_target_visitor: IDrdTestTargetVisitor = NullDrdTestTargetVisitor(),
        helgrind_test_target_visitor: IHelgrindTestTargetVisitor = NullHelgrindTestTargetVisitor(),
        memcheck_test_target_visitor: IMemcheckTestTargetVisitor = NullMemcheckTestTargetVisitor()):
        """
        Initializes a new instance of the VisitorSet class.
        @param project_visitor The visitor that will be applied to projects.
        @param project_scope_visitor The visitor that will be applied to project
          scopes.
        @param build_target_visitor The visitor that will be applied to build
          targets.
        @param executable_target_visitor The visitor that will be applied to
          executable targets.
        @param library_target_visitor The visitor that will be applied to
          library targets.
        @param static_library_target_visitor The visitor that will be applied to
          static library targets.
        @param shared_library_target_visitor The visitor that will be applied to
          shared library targets.
        @param documentation_target_visitor The visitor that will be applied to
          documentation targets.
        @param doxygen_target_visitor The visitor that will be applied to
          doxygen targets.
        @param imported_target_visitor The visitor that will be applied to
          imported targets.
        @param external_library_target_visitor The visitor that will be applied
          to external library targets.
        @param test_target_visitor The visitor that will be applied to test
          targets.
        @param gtest_target_visitor The visitor that will be applied to gtest
          targets.
        @param test_wrapper_target_visitor The visitor that will be applied to
          test wrapper targets.
        @param valgrind_test_target_visitor The visitor that will be applied to
          valgrind test targets.
        @param drd_test_target_visitor The visitor that will be applied to drd
          test targets.
        @param helgrind_test_target_visitor The visitor that will be applied to
          helgrind test targets.
        @param memcheck_test_target_visitor The visitor that will be applied to
          memcheck test targets.
        """
        self._project_visitor = project_visitor
        self._project_scope_visitor = project_scope_visitor
        self._build_target_visitor = build_target_visitor
        self._executable_target_visitor = executable_target_visitor
        self._library_target_visitor = library_target_visitor
        self._static_library_target_visitor = static_library_target_visitor
        self._shared_library_target_visitor = shared_library_target_visitor
        self._documentation_target_visitor = documentation_target_visitor
        self._doxygen_target_visitor = doxygen_target_visitor
        self._imported_target_visitor = imported_target_visitor
        self._external_library_target_visitor = external_library_target_visitor
        self._test_target_visitor = test_target_visitor
        self._gtest_target_visitor = gtest_target_visitor
        self._test_wrapper_target_visitor = test_wrapper_target_visitor
        self._valgrind_test_target_visitor = valgrind_test_target_visitor
        self._drd_test_target_visitor = drd_test_target_visitor
        self._helgrind_test_target_visitor = helgrind_test_target_visitor
        self._memcheck_test_target_visitor = memcheck_test_target_visitor


    @property
    def project_visitor(self) -> IProjectVisitor:
        """
        Gets the visitor that will be applied to projects.
        """
        return self._project_visitor


    @property
    def project_scope_visitor(self) -> IProjectScopeVisitor:
        """
        Gets the visitor that will be applied to project scopes.
        """
        return self._project_scope_visitor


    @property
    def build_target_visitor(self) -> IBuildTargetVisitor:
        """
        Gets the visitor that will be applied to build targets.
        """
        return self._build_target_visitor


    @property
    def executable_target_visitor(self) -> IExecutableTargetVisitor:
        """
        Gets the visitor that will be applied to executable targets.
        """
        return self._executable_target_visitor


    @property
    def library_target_visitor(self) -> ILibraryTargetVisitor:
        """
        Gets the visitor that will be applied to library targets.
        """
        return self._library_target_visitor


    @property
    def static_library_target_visitor(self) -> IStaticLibraryTargetVisitor:
        """
        Gets the visitor that will be applied to static library targets.
        """
        return self._static_library_target_visitor


    @property
    def shared_library_target_visitor(self) -> ISharedLibraryTargetVisitor:
        """
        Gets the visitor that will be applied to shared library targets.
        """
        return self._shared_library_target_visitor


    @property
    def documentation_target_visitor(self) -> IDocumentationTargetVisitor:
        """
        Gets the visitor that will be applied to documentation targets.
        """
        return self._documentation_target_visitor


    @property
    def doxygen_target_visitor(self) -> IDoxygenTargetVisitor:
        """
        Gets the visitor that will be applied to doxygen targets.
        """
        return self._doxygen_target_visitor


    @property
    def imported_target_visitor(self) -> IImportedTargetVisitor:
        """
        Gets the visitor that will be applied to imported targets.
        """
        return self._imported_target_visitor


    @property
    def external_library_target_visitor(self) -> IExternalLibraryTargetVisitor:
        """
        Gets the visitor that will be applied to external library targets.
        """
        return self._external_library_target_visitor


    @property
    def test_target_visitor(self) -> ITestTargetVisitor:
        """
        Gets the visitor that will be applied to test targets.
        """
        return self._test_target_visitor


    @property
    def gtest_target_visitor(self) -> IGTestTargetVisitor:
        """
        Gets the visitor that will be applied to gtest targets.
        """
        return self._gtest_target_visitor


    @property
    def test_wrapper_target_visitor(self) -> ITestWrapperTargetVisitor:
        """
        Gets the visitor that will be applied to test wrapper targets.
        """
        return self._test_wrapper_target_visitor


    @property
    def valgrind_test_target_visitor(self) -> IValgrindTestTargetVisitor:
        """
        Gets the visitor that will be applied to valgrind test targets.
        """
        return self._valgrind_test_target_visitor


    @property
    def drd_test_target_visitor(self) -> IDrdTestTargetVisitor:
        """
        Gets the visitor that will be applied to drd test targets.
        """
        return self._drd_test_target_visitor


    @property
    def helgrind_test_target_visitor(self) -> IHelgrindTestTargetVisitor:
        """
        Gets the visitor that will be applied to helgrind test targets.
        """
        return self._helgrind_test_target_visitor


    @property
    def memcheck_test_target_visitor(self) -> IMemcheckTestTargetVisitor:
        """
        Gets the visitor that will be applied to memcheck test targets.
        """
        return self._memcheck_test_target_visitor

