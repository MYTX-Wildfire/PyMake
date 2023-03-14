from pymake.common.sanitizer_flags import ESanitizerFlags
from pymake.common.target_type import ETargetType
from pymake.common.test_flags import ETestFlags
from pymake.model.targets.build.interface_target import InterfaceTarget
from pymake.model.targets.build.build_target import BuildTarget
from pymake.model.targets.build.executable_target import ExecutableTarget
from pymake.model.targets.build.library_target import LibraryTarget
from pymake.model.targets.build.shared_library_target import SharedLibraryTarget
from pymake.model.targets.build.static_library_target import StaticLibraryTarget
from pymake.model.targets.imported.imported_target import ImportedTarget
from pymake.model.targets.docs.documentation_target import DocumentationTarget
from pymake.model.targets.docs.doxygen_target import DoxygenTarget
from pymake.model.targets.imported.imported_target import ImportedTarget
from pymake.model.targets.test.drd_test_target import DrdTestTarget
from pymake.model.targets.test.gtest_target import GTestTarget
from pymake.model.targets.test.helgrind_test_target import HelgrindTestTarget
from pymake.model.targets.test.memcheck_test_target import MemcheckTestTarget
from pymake.model.targets.test.test_target import TestTarget
from pymake.model.targets.test.test_wrapper_target import TestWrapperTarget
from pymake.model.targets.target import Target
from pymake.tracing.traced import ITraced
from pymake.tracing.traced_dict import TracedDict
from typing import Iterable, Optional, TypeVar

TargetType = TypeVar("TargetType", bound=Target)

class TargetSet(ITraced):
    """
    Groups logically identical targets together.
    """
    def __init__(self,
        set_name: str,
        all_target_name: str,
        test_target_name: str,
        common_target_name: str):
        """
        Initializes the target set.
        @param set_name Name of the target set.
        @param all_target_name Name of the target that builds all targets in the
          set.
        @param test_target_name Name of the target that builds all test targets
          in the set.
        @param common_target_name Name of the set's common interface target.
        """
        super().__init__()

        self._set_name = set_name
        self._all_target_name = all_target_name
        self._test_target_name = test_target_name

        ## All targets in the set.
        # Each target is indexed by its name.
        self._targets: TracedDict[str, Target] = TracedDict()

        ## All built targets in the set.
        # Each target is indexed by its name.
        self._built_targets: TracedDict[str, BuildTarget] = TracedDict()

        ## All executable targets in the set.
        # Each target is indexed by its name.
        # @warning This collection contains only non-test executable targets
        #   that are built by the set.
        self._executable_targets: TracedDict[str, ExecutableTarget] = \
            TracedDict()

        ## All library (shared or static) targets in the set.
        # Each target is indexed by its name.
        # @remarks This collection does not include imported library targets.
        self._library_targets: TracedDict[str, LibraryTarget] = TracedDict()

        ## All static library targets in the set.
        # Each target is indexed by its name.
        # @remarks This collection does not include imported static library
        #   targets.
        self._static_library_targets: TracedDict[str, StaticLibraryTarget] = \
            TracedDict()

        ## All shared library targets in the set.
        # Each target is indexed by its name.
        # @remarks This collection does not include imported shared library
        #   targets.
        self._shared_library_targets: TracedDict[str, SharedLibraryTarget] = \
            TracedDict()

        ## All imported targets in the set.
        # Each target is indexed by its name.
        self._imported_targets: TracedDict[str, ImportedTarget] = TracedDict()

        ## All sanitized targets in the set.
        # Each target is indexed by its name.
        self._sanitized_targets: TracedDict[str, Target] = TracedDict()

        ## List of all test targets in the set.
        # Each target is indexed by its name.
        self._test_targets: TracedDict[str, Target] = TracedDict()

        ## List of all documentation targets in the set.
        # Each target is indexed by its name.
        self._documentation_targets: TracedDict[str, DocumentationTarget] = \
            TracedDict()

        ## Common target for the set.
        self._common_target = InterfaceTarget(common_target_name)
        self._targets[common_target_name] = self._common_target


    @property
    def set_name(self) -> str:
        """
        Gets the name of the target set.
        """
        return self._set_name


    @property
    def all_target_name(self) -> str:
        """
        Gets the name of the target that builds all targets in the set.
        """
        return self._all_target_name


    @property
    def test_target_name(self) -> str:
        """
        Gets the name of the target that builds all test targets in the set.
        """
        return self._test_target_name


    @property
    def common_target(self) -> InterfaceTarget:
        """
        Gets the common target for the set.
        """
        return self._common_target


    @property
    def targets(self) -> Iterable[Target]:
        """
        Gets all targets in the set.
        """
        return list(self._targets.values())


    @property
    def built_targets(self) -> Iterable[BuildTarget]:
        """
        Gets all built targets in the set.
        """
        return list(self._built_targets.values())


    @property
    def executable_targets(self) -> Iterable[ExecutableTarget]:
        """
        Gets all executable targets in the set.
        """
        return list(self._executable_targets.values())


    @property
    def library_targets(self) -> Iterable[LibraryTarget]:
        """
        Gets all library targets in the set.
        """
        return list(self._library_targets.values())


    @property
    def static_library_targets(self) -> Iterable[StaticLibraryTarget]:
        """
        Gets all static library targets in the set.
        """
        return list(self._static_library_targets.values())


    @property
    def shared_library_targets(self) -> Iterable[SharedLibraryTarget]:
        """
        Gets all shared library targets in the set.
        """
        return list(self._shared_library_targets.values())


    @property
    def imported_targets(self) -> Iterable[ImportedTarget]:
        """
        Gets all imported targets in the set.
        """
        return list(self._imported_targets.values())


    @property
    def sanitized_targets(self) -> Iterable[Target]:
        """
        Gets all sanitized targets in the set.
        """
        return list(self._sanitized_targets.values())


    @property
    def test_targets(self) -> Iterable[Target]:
        """
        Gets all test targets in the set.
        """
        return list(self._test_targets.values())


    @property
    def documentation_targets(self) -> Iterable[DocumentationTarget]:
        """
        Gets all documentation targets in the set.
        """
        return list(self._documentation_targets.values())


    def add_executable(self,
        target_name: str,
        sanitizer_flags: int) -> ExecutableTarget:
        """
        Adds a non-test executable target to the set.
        @param target_name Name of the target.
        @param sanitizer_flags Flags indicating which sanitizers are enabled
          for the target.
        @throws RuntimeError Thrown if a target with the same name already
          exists and was added at a different location.
        @returns The target that was added. If the target already exists and
          was added at the same location, the existing target is returned.
        """
        return self._add_new_target(ExecutableTarget(
            target_name,
            ETestFlags.NONE,
            sanitizer_flags
        ))


    def add_external_static_library(self,
        target_name: str,
        sanitizer_flags: int) -> ImportedTarget:
        """
        Adds an externally built static library target to the set.
        @param target_name Name of the target.
        @param sanitizer_flags Flags indicating which sanitizers are enabled
          for the target.
        @throws RuntimeError Thrown if a target with the same name already
          exists and was added at a different location.
        @returns The target that was added. If the target already exists and
          was added at the same location, the existing target is returned.
        """
        return self._add_new_target(ImportedTarget(
            target_name,
            ETargetType.STATIC,
            sanitizer_flags
        ))


    def add_static_library(self,
        target_name: str,
        sanitizer_flags: int) -> StaticLibraryTarget:
        """
        Adds a static library target to the set.
        @param target_name Name of the target.
        @param sanitizer_flags Flags indicating which sanitizers are enabled
          for the target.
        @throws RuntimeError Thrown if a target with the same name already
          exists and was added at a different location.
        @returns The target that was added. If the target already exists and
          was added at the same location, the existing target is returned.
        """
        return self._add_new_target(StaticLibraryTarget(
            target_name,
            sanitizer_flags
        ))


    def add_shared_library(self,
        target_name: str,
        sanitizer_flags: int) -> SharedLibraryTarget:
        """
        Adds a shared library target to the set.
        @param target_name Name of the target.
        @param sanitizer_flags Flags indicating which sanitizers are enabled
          for the target.
        @throws RuntimeError Thrown if a target with the same name already
          exists and was added at a different location.
        @returns The target that was added. If the target already exists and
          was added at the same location, the existing target is returned.
        """
        return self._add_new_target(SharedLibraryTarget(
            target_name,
            sanitizer_flags
        ))


    def add_imported_target(self,
        target_name: str,
        target_type: ETargetType,
        sanitizer_flags: int) -> ImportedTarget:
        """
        Adds an imported target to the set.
        @param target_name Name of the target.
        @param target_type Type of the imported target.
        @param sanitizer_flags Flags indicating which sanitizers are enabled
          for the target.
        @throws RuntimeError Thrown if a target with the same name already
          exists and was added at a different location.
        @returns The target that was added. If the target already exists and
          was added at the same location, the existing target is returned.
        """
        return self._add_new_target(ImportedTarget(
            target_name,
            target_type,
            sanitizer_flags
        ))


    def add_gtest_executable(self,
        target_name: str,
        test_flags: int,
        sanitizer_flags: int) -> GTestTarget:
        """
        Adds a test executable target to the set.
        @param target_name Name of the target.
        @param test_flags Flags indicating properties of the test executable.
        @param sanitizer_flags Flags indicating which sanitizers are enabled
          for the target.
        @throws RuntimeError Thrown if a target with the same name already
          exists and was added at a different location.
        @returns The target that was added. If the target already exists and
          was added at the same location, the existing target is returned.
        """
        return self._add_new_target(GTestTarget(
            target_name,
            test_flags,
            sanitizer_flags
        ))


    def add_drd_target(self,
        target_name: str,
        wrapped_target: ExecutableTarget) -> DrdTestTarget:
        """
        Adds a Valgrind DRD test target to the set.
        @param target_name Name of the target.
        @param wrapped_target Executable to invoke with DRD.
        @throws RuntimeError Thrown if a target with the same name already
          exists and was added at a different location.
        @returns The target that was added. If the target already exists and
          was added at the same location, the existing target is returned.
        """
        return self._add_new_target(DrdTestTarget(
            target_name,
            wrapped_target
        ))


    def add_helgrind_target(self,
        target_name: str,
        wrapped_target: ExecutableTarget) -> HelgrindTestTarget:
        """
        Adds a Valgrind Helgrind test target to the set.
        @param target_name Name of the target.
        @param wrapped_target Executable to invoke with Helgrind.
        @throws RuntimeError Thrown if a target with the same name already
          exists and was added at a different location.
        @returns The target that was added. If the target already exists and
          was added at the same location, the existing target is returned.
        """
        return self._add_new_target(HelgrindTestTarget(
            target_name,
            wrapped_target
        ))


    def add_memcheck_target(self,
        target_name: str,
        wrapped_target: ExecutableTarget) -> MemcheckTestTarget:
        """
        Adds a Valgrind Memcheck test target to the set.
        @param target_name Name of the target.
        @param wrapped_target Executable to invoke with Memcheck.
        @throws RuntimeError Thrown if a target with the same name already
          exists and was added at a different location.
        @returns The target that was added. If the target already exists and
          was added at the same location, the existing target is returned.
        """
        return self._add_new_target(MemcheckTestTarget(
            target_name,
            wrapped_target
        ))


    def add_doxygen_target(self,
        target_name: str) -> DoxygenTarget:
        """
        Adds a Doxygen target to the set.
        @param target_name Name of the target.
        @throws RuntimeError Thrown if a target with the same name already
          exists and was added at a different location.
        @returns The target that was added. If the target already exists and
          was added at the same location, the existing target is returned.
        """
        return self._add_new_target(DoxygenTarget(
            target_name
        ))


    def _add_new_target(self,
        new_target: TargetType) -> TargetType:
        """
        Adds a new target to the set.
        @param new_target Target to add.
        @throws RuntimeError Thrown if a target with the same name already
          exists and was added at a different location.
        @returns The target that was added. If the target already exists and
          was added at the same location, the existing target is returned.
        """
        # Check if the target already exists
        prev_target = self._get_prev_target(new_target)
        if prev_target:
            return prev_target

        # Keep track of whether the target should be linked to the target set's
        #   common target
        link_to_common = False

        # Add the target
        self._targets[new_target.target_name] = new_target
        if isinstance(new_target, TestTarget):
            self._test_targets[new_target.target_name] = new_target
            self._built_targets[new_target.target_name] = new_target
            link_to_common = True
        elif isinstance(new_target, ExecutableTarget):
            self._executable_targets[new_target.target_name] = new_target
            self._built_targets[new_target.target_name] = new_target
            link_to_common = True
        elif isinstance(new_target, TestWrapperTarget):
            self._test_targets[new_target.target_name] = new_target
        elif isinstance(new_target, StaticLibraryTarget):
            self._library_targets[new_target.target_name] = new_target
            self._static_library_targets[new_target.target_name] = new_target
            self._built_targets[new_target.target_name] = new_target
            link_to_common = True
        elif isinstance(new_target, SharedLibraryTarget):
            self._library_targets[new_target.target_name] = new_target
            self._shared_library_targets[new_target.target_name] = new_target
            self._built_targets[new_target.target_name] = new_target
            link_to_common = True
        elif isinstance(new_target, ImportedTarget):
            self._imported_targets[new_target.target_name] = new_target
        elif isinstance(new_target, DocumentationTarget):
            self._documentation_targets[new_target.target_name] = new_target

        if new_target.sanitizer_flags != ESanitizerFlags.NONE:
            self._sanitized_targets[new_target.target_name] = new_target

        # Link the target to the target set's common target if necessary
        if link_to_common:
            new_target.properties.link_libraries.private.add(
                self._common_target.target_name
            )

        return new_target


    def _get_prev_target(self,
        new_target: TargetType) -> Optional[TargetType]:
        """
        Gets the previously created target if it exists.
        @param new_target Target potentially being added.
        @throws RuntimeError Thrown if a target with the same name already
          exists and was added at a different location.
        @returns If a target with the same name already exists and was added
          at the same location, the existing target is returned. Otherwise,
          None is returned.
        """
        if new_target.target_name not in self._targets:
            return None

        # Check if the target was added from the same location
        # Note that it doesn't matter if the target is the same type as the
        #   new target because adding a target with the same name from two
        #   different locations is an error regardless of whether the target
        #   types are the same.
        # This also means that the target type doesn't need to be checked since
        #   if the previous target was added at the same location as the new
        #   target, the two targets must be the same type.
        prev_target = self._targets[new_target.target_name]
        if prev_target.origin != new_target.origin:
            error_str = "Error: Cannot add a target with the name " + \
                f"'{new_target.target_name}' to the target set " + \
                f"'{self._set_name}'.\n"
            error_str += "Note: A target with the name " + \
                f"'{new_target.target_name}' already exists in the target set.\n"
            error_str += "    The target was previously added at " + \
                f"{prev_target.origin.file_path}:" + \
                f"{prev_target.origin.line_number}.\n"
            error_str += "    The new target is being added at " + \
                f"{new_target.origin.file_path}:" + \
                f"{new_target.origin.line_number}."
            raise RuntimeError(error_str)

        assert type(prev_target) == type(new_target)
        return prev_target
