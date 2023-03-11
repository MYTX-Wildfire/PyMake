from pymake.common.sanitizer_flags import ESanitizerFlags
from pymake.common.scope import EScope
from pymake.core.build_script import BuildScript
from pymake.model.targets.build.executable_target import ExecutableTarget
from pymake.model.targets.build.library_target import LibraryTarget
from pymake.model.targets.interface_target import InterfaceTarget
from pymake.model.targets.target import Target
from pymake.tracing.traced_dict import TracedDict
from typing import Callable, Dict, Generic, Iterable, List, Optional, TypeVar

LibraryType = TypeVar("LibraryType", bound=LibraryTarget)

class InternalLibrarySet(Generic[LibraryType]):
    """
    Groups a library with its associated sanitizer and test targets.
    This is a helper class meant for internal use only to reduce code
      duplication in the `LibrarySet` class.
    """
    def __init__(self,
        target_set_name: str,
        common_target: InterfaceTarget,
        library_factory: Callable[[str, int], LibraryType]):
        """
        Initializes the library set.
        @param target_set_name Name of the library set. This should be the name
          of the library set that owns this instance.
        @param common_target The common target for the library set.
        @param library_factory A function that creates a library target with
          the given name and sanitizer flags.
        """
        self._target_set_name = target_set_name
        self._common_target = common_target
        self._create_library_target = library_factory

        # Primary library target for the set
        self._library_target: Optional[LibraryType] = None

        ## Collection of sanitized targets, indexed by target name
        self._sanitized_targets: TracedDict[str, LibraryType] = TracedDict()

        ## Collection of test targets, indexed by target name
        self._test_targets: TracedDict[str, ExecutableTarget] = TracedDict()

        ## Sanitized targets, indexed by sanitizer flag
        # This is used to keep track of whether a sanitized target has been
        #   added for each sanitizer flag. Adding two sanitized targets with
        #   the same sanitizer flag has no added benefit, so this class assumes
        #   that adding two sanitized targets with the same sanitizer flag is
        #   an error.
        self._sanitized_targets_by_flag: \
            Dict[ESanitizerFlags, Optional[LibraryType]] = {}
        for sanitizer_flag in ESanitizerFlags:
            if sanitizer_flag == ESanitizerFlags.NONE:
                continue
            self._sanitized_targets_by_flag[sanitizer_flag] = None


    @property
    def targets(self) -> Iterable[Target]:
        """
        Gets the targets in this target set.
        """
        targets: List[Target] = []
        if self._library_target:
            targets.append(self._library_target)
        targets.extend([t for _, t in self._sanitized_targets])
        targets.extend([t for _, t in self._test_targets])
        return targets


    def add_base_target(self, target_name: str) -> LibraryType:
        """
        Sets the library set's base library target.
        @param target The base library target to add.
        @throws RuntimeError If a base target already exists and was added at
          a different location.
        @returns The base library target. This will either be a previously added
          base target or the target passed in. This target will be configured to
          link to the common target.
        """
        target = self._create_library_target(target_name, ESanitizerFlags.NONE)

        if self._library_target:
            # If the previously added base target was added at the same location
            #   as the target passed in, then return the previously added base
            #   target. Otherwise, raise an error.
            if self._library_target.origin == target.origin:
                return self._library_target

            error_str = "Error: A target with the name " + \
                f"'{target.target_name}' already exists.\n"
            error_str += "Note: The target was previously added at " + \
                f"{self._library_target.origin.file_path}:" + \
                f"{self._library_target.origin.line_number}\n"
            error_str += "Note: Target is being redefined at " + \
                f"{target.origin.file_path}:" + \
                f"{target.origin.line_number}"
            raise RuntimeError(error_str)

        self._library_target = target
        target.link_to(EScope.PUBLIC, self._common_target)
        return target


    def add_sanitized_target(self,
        target_name: str,
        sanitizer_flags: int) -> LibraryType:
        """
        Adds a sanitized target to the library set.
        @warning This method will *not* add the flags required to enable
          sanitizers to the returned target.
        @param target_name Name of the sanitized target to add.
        @param sanitizer_flags Sanitizer flags to use for the sanitized target.
        @throws RuntimeError If the base target has not been added.
        @throws RuntimeError If the sanitized target already exists with the
          given target name and was added at a different location.
        @throws RuntimeError If a sanitized target already exists with the
          same sanitizer flags.
        @returns The sanitized target. This will either be a previously added
          sanitized target or a newly created sanitized target. This target will
          be configured to link against the base target.
        """
        if not self._library_target:
            raise RuntimeError("Error: The base target has not been added.")

        sanitized_target = self._create_library_target(
            target_name,
            sanitizer_flags
        )

        # Check if a sanitized target with the same name has already been added
        if target_name in self._sanitized_targets:
            # If the previously added sanitized target was added at the same
            #   location as the target passed in, then return the previously
            #   added sanitized target. Otherwise, raise an error.
            if self._sanitized_targets[target_name].origin == \
                sanitized_target.origin:
                return self._sanitized_targets[target_name]

            error_str = "Error: A target with the name " + \
                f"'{target_name}' already exists.\n"
            error_str += "Note: The target was previously added at " + \
                f"{self._sanitized_targets[target_name].origin.file_path}:" + \
                f"{self._sanitized_targets[target_name].origin.line_number}\n"
            error_str += "Note: Target is being redefined at " + \
                f"{sanitized_target.origin.file_path}:" + \
                f"{sanitized_target.origin.line_number}"
            raise RuntimeError(error_str)

        # Check if a sanitized target with the same sanitizer flag has already
        #   been added
        for flag in ESanitizerFlags:
            if flag == ESanitizerFlags.NONE:
                continue

            if not sanitizer_flags & flag:
                continue

            if self._sanitized_targets_by_flag[flag]:
                prev_target = self._sanitized_targets_by_flag[flag]
                assert prev_target is not None

                error_str = "Error: A sanitized target with the " + \
                    f"sanitizer flag '{flag.name}' already exists.\n"
                error_str += "Note: The target was previously added at " + \
                    f"{prev_target.origin.file_path}:" + \
                    f"{prev_target.origin.line_number}\n"
                error_str += "Note: The new target is being added at " + \
                    f"{sanitized_target.origin.file_path}:" + \
                    f"{sanitized_target.origin.line_number}"
                raise RuntimeError(error_str)

        # Add the sanitized target
        self._sanitized_targets[target_name] = sanitized_target
        for flag in ESanitizerFlags:
            if flag == ESanitizerFlags.NONE:
                continue

            if sanitizer_flags & flag:
                self._sanitized_targets_by_flag[flag] = sanitized_target

        # Configure the sanitized target to link against the base target
        sanitized_target.link_to(EScope.PUBLIC, self._library_target)

        return sanitized_target


    def add_test_target(self,
        target_name: str,
        test_flags: int,
        sanitizer_flags: int) -> ExecutableTarget:
        """
        Adds a test target to the library set.
        @warning This method will *not* add the flags required to enable
          sanitizers to the returned target.
        @param target_name Name of the test target to add.
        @param test_flags Test flags to use for the test target.
        @param sanitizer_flags Sanitizer flags to use for the test target.
        @throws RuntimeError If the base target has not been added.
        @throws ValueError If a test target already exists with the same name
          and was added at a different location.
        @returns The test target. This will either be a previously added test
          target or a newly created test target. The target will be configured
          to link publicly with the base target.
        """
        if not self._library_target:
            raise RuntimeError("Error: The base target has not been added.")

        test_target = ExecutableTarget(
            target_name,
            test_flags,
            sanitizer_flags
        )

        # Check if a test target with the same name has already been added
        if target_name in self._test_targets:
            # If the previously added test target was added at the same location
            #   as the target passed in, then return the previously added test
            #   target. Otherwise, raise an error.
            if self._test_targets[target_name].origin == test_target.origin:
                return self._test_targets[target_name]

            prev_target = self._test_targets[target_name]
            error_str = "Error: A target with the name " + \
                f"'{target_name}' already exists.\n"
            error_str += "Note: The target was previously added at " + \
                f"{prev_target.origin.file_path}:" + \
                f"{prev_target.origin.line_number}\n"
            error_str += "Note: The new target is being added at " + \
                f"{test_target.origin.file_path}:" + \
                f"{test_target.origin.line_number}"
            raise ValueError(error_str)

        # Add the test target
        self._test_targets[target_name] = test_target

        # Configure the test target to link against the base target
        test_target.link_to(EScope.PUBLIC, self._library_target)

        return test_target


    def generate_library_set(self,
        build_script: BuildScript):
        """
        Generates the CMake code for the set.
        @param build_script The build script to write the library set's CMake
          code to.
        """
        # Generate the primary target before any other target
        if self._library_target:
            self._library_target.generate_target(build_script)

        # Generate the sanitized targets
        for _, target in self._sanitized_targets:
            target.generate_target(build_script)

        # Generate the test targets
        for _, target in self._test_targets:
            target.generate_target(build_script)
