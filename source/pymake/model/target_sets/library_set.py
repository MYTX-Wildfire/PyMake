from pymake.core.build_script import BuildScript
from pymake.model.target_sets.internal_library_set import InternalLibrarySet
from pymake.model.target_sets.target_set import ITargetSet
from pymake.model.targets.build.executable_target import ExecutableTarget
from pymake.model.targets.build.shared_library_target import SharedLibraryTarget
from pymake.model.targets.build.static_library_target import StaticLibraryTarget
from pymake.model.targets.interface_target import InterfaceTarget
from pymake.model.targets.target import Target
from typing import Iterable, List, Optional

class LibrarySet(ITargetSet):
    """
    Groups a library with its associated sanitizer and test targets.
    """
    def __init__(self,
        target_set_name: str,
        common_target_name: Optional[str],
        common_target_suffix: str = "-common"):
        """
        Initializes the set.
        @param target_set_name The name of the target set.
        @param common_target_name The name to use for the common target. If
          None, the common target name will be the target set name plus
          `common_target_suffix`.
        @param common_target_suffix The suffix to append to target set name if
          `common_target_name` is None.
        """
        # Create the common target
        if common_target_name is None:
            common_target_name = target_set_name + common_target_suffix
        self._common_target = InterfaceTarget(common_target_name)

        # Create the static library set
        self._static_library_set = InternalLibrarySet(
            target_set_name,
            self._common_target,
            lambda target_name, sanitizer_flags: \
                StaticLibraryTarget(target_name, sanitizer_flags)
        )

        # Create the shared library set
        self._shared_library_set = InternalLibrarySet(
            target_set_name,
            self._common_target,
            lambda target_name, sanitizer_flags: \
                SharedLibraryTarget(target_name, sanitizer_flags)
        )


    @property
    def common_target(self) -> InterfaceTarget:
        """
        Gets the common target for the set.
        @note All targets in the set will link to this target automatically.
        """
        return self._common_target


    def add_static_library(self,
        target_name: str) -> StaticLibraryTarget:
        """
        Adds the base static library target to the set.
        @param target_name The name of the target.
        @throws RuntimeError If a base target already exists and was added at
          a different location.
        @returns The base library target. This will either be a previously added
          base target or a newly constructed target. This target will be
          configured to link to the common target.
        """
        return self._static_library_set.add_base_target(target_name)


    def add_shared_library(self,
        target_name: str) -> SharedLibraryTarget:
        """
        Adds the base shared library target to the set.
        @param target_name The name of the target.
        @throws RuntimeError If a base target already exists and was added at
          a different location.
        @returns The base library target. This will either be a previously added
          base target or a newly constructed target. This target will be
          configured to link to the common target.
        """
        return self._shared_library_set.add_base_target(target_name)


    def add_sanitized_static_library(self,
        target_name: str,
        sanitizer_flags: int) -> StaticLibraryTarget:
        """
        Adds a sanitized static library target to the set.
        @warning This method will *not* add the flags required to enable
          sanitizers to the returned target.
        @param target_name The name of the target.
        @param sanitizer_flags The sanitizer flags to use for the target.
        @throws RuntimeError If the base static library target has not been
          added.
        @throws RuntimeError If the sanitized target already exists with the
          given target name and was added at a different location.
        @throws RuntimeError If a sanitized target already exists with the
          same sanitizer flags.
        @returns The sanitized library target. This will either be a previously
          added sanitized target or a newly constructed target. This target will
          be configured to link to the common and the base library target.
        """
        return self._static_library_set.add_sanitized_target(
            target_name,
            sanitizer_flags
        )


    def add_sanitized_shared_library(self,
        target_name: str,
        sanitizer_flags: int) -> SharedLibraryTarget:
        """
        Adds a sanitized shared library target to the set.
        @warning This method will *not* add the flags required to enable
          sanitizers to the returned target.
        @param target_name The name of the target.
        @param sanitizer_flags The sanitizer flags to use for the target.
        @throws RuntimeError If the base shared library target has not been
          added.
        @throws RuntimeError If the sanitized target already exists with the
          given target name and was added at a different location.
        @throws RuntimeError If a sanitized target already exists with the
          same sanitizer flags.
        @returns The sanitized library target. This will either be a previously
          added sanitized target or a newly constructed target. This target will
          be configured to link to the common and the base library target.
        """
        return self._shared_library_set.add_sanitized_target(
            target_name,
            sanitizer_flags
        )


    def add_test_target(self,
        target_name: str,
        test_flags: int,
        sanitizer_flags: int,
        link_to_static: bool) -> ExecutableTarget:
        """
        Adds a test target to the set.
        @warning This method will *not* add the flags required to enable
          sanitizers to the returned target.
        @param target_name The name of the target.
        @param test_flags The test flags to use for the target.
        @param sanitizer_flags The sanitizer flags to use for the target.
        @param link_to_static If True, the test target will link to the static
          library target. If False, the test target will link to the shared
          library target.
        @throws RuntimeError If the base library target has not been added.
        @throws RuntimeError If the test target already exists with the given
          target name and was added at a different location.
        @throws RuntimeError If a test target already exists with the same
          sanitizer flags.
        @returns The test target. This will either be a previously added test
          target or a newly constructed target. This target will be configured
          to link to the common target and the base library target.
        """
        if link_to_static:
            return self._static_library_set.add_test_target(
                target_name,
                test_flags,
                sanitizer_flags
            )

        return self._shared_library_set.add_test_target(
            target_name,
            test_flags,
            sanitizer_flags
        )


    @property
    def targets(self) -> Iterable[Target]:
        """
        Gets the targets in this target set.
        """
        targets: List[Target] = []
        targets.append(self._common_target)
        targets.extend(self._static_library_set.targets)
        targets.extend(self._shared_library_set.targets)
        return targets
