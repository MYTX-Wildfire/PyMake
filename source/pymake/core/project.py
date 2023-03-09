from pymake.common.project_language import EProjectLanguage
from pymake.core.build_script_set import BuildScriptSet
from pymake.targets.executable_target import ExecutableTarget
from pymake.targets.gtest_target import GoogleTestTarget
from pymake.targets.shared_library_target import SharedLibraryTarget
from pymake.targets.static_library_target import StaticLibraryTarget
from pymake.targets.test_target import TestTarget
from pymake.targets.target import ITarget
from pymake.tracing.traced import ITraced
from typing import Callable, Dict, Iterable, Optional

class Project(ITraced):
    """
    Represents a single project scope in a PyMake project.
    """
    def __init__(self,
        build_scripts: BuildScriptSet,
        project_name: str,
        project_languages: EProjectLanguage | Iterable[EProjectLanguage],
        enable_ctest: bool = True,
        project_all_target_name: Optional[str] = None,
        project_all_suffix: str = "-all",
        project_test_target_name: Optional[str] = None,
        project_test_suffix: str = "-test",):
        """
        Initializes the project.
        @param build_scripts Set of build scripts that the project will generate.
        @param project_name Name of the project.
        @param project_languages Languages used in the project.
        @param enable_ctest Whether to enable CTest for the project.
        @param project_all_target_name Name of the project-specific `all`
          target. If `None`, the project's `all` target will be named
          `[project_name][project_all_suffix]`.
        @param project_all_suffix Suffix to append to the project name to
          generate the project's `all` target name.
        @param project_test_target_name Name of the project-specific `test`
          target. If `None`, the project's `test` target will be named
          `[project_name][project_test_suffix]`.
        @param project_test_suffix Suffix to append to the project name to
          generate the project's `test` target name.
        """
        super().__init__()
        self._build_scripts = build_scripts
        self._project_name = project_name
        self._project_languages = list(project_languages) if isinstance(
            project_languages, Iterable) else [project_languages]

        # Figure out what name should be used for the project's `all` and `test`
        #   targets
        if project_all_target_name is None:
            project_all_target_name = f"{project_name}{project_all_suffix}"
        if project_test_target_name is None:
            project_test_target_name = f"{project_name}{project_test_suffix}"
        self._project_all_target_name = project_all_target_name
        self._project_test_target_name = project_test_target_name

        # Callback that will be invoked when a target is added
        # The callback will be passed the target that was just added as its only
        #   parameter. If a target was already added with the given name, the
        #   previously added target must be returned.
        self._on_target_added: Callable[[ITarget], Optional[ITarget]] = \
            lambda target: None

        # Collections of untraced values
        # These values are stored as-is instead of in `Traced` objects since
        #   each instance manages its own tracing information
        self._targets: Dict[str, ITarget] = {}

        # Collection of targets that the project's `test` target must rely on
        # All targets in this collection will also be in `self._targets`.
        self._test_targets: Dict[str, TestTarget] = {}

        # Generate the CMake code
        generator = self._build_scripts.get_or_add_build_script().generator
        with generator.open_method_block("project") as b:
            b.add_arguments(self._project_name)
            b.add_keyword_arguments(
                "LANGUAGES",
                *[l.value for l in self._project_languages]
            )

        # Generate the project's `all` target
        with generator.open_method_block("add_custom_target") as b:
            b.add_arguments(self._project_all_target_name)
            # Since the target doesn't build anything directly, add it to the
            #   `ALL` build target for completeness
            b.add_arguments("ALL")

        self._enable_ctest = enable_ctest
        if enable_ctest:
            # Enable CTest
            with generator.open_method_block("include") as b:
                b.add_arguments("CTest")
            with generator.open_method_block("enable_testing") as b:
                pass

            # Generate the project's `test` target
            with generator.open_method_block("add_custom_target") as b:
                b.add_arguments(self._project_test_target_name)
                # Since the target doesn't build anything directly, add it to the
                #   `ALL` build target for completeness
                b.add_arguments("ALL")

            # If testing is enabled, set up a fixture that forces CMake to build
            #   the test targets before running the tests
            # CMake's default behavior is to not build the test targets before
            #   trying to run them. This behavior has been reported as a bug in
            #   2009, but CMake has yet to introduce a (dedicated) workaround
            #   for this behavior:
            #   https://gitlab.kitware.com/cmake/cmake/-/issues/8774
            # To get around this, use CMake fixtures as mentioned here:
            #   https://stackoverflow.com/a/56448477

            # Name used for the target that the test fixture builds
            self._fixture_target_name = \
                "\"pymake-internal-build-tests-fixture-target-" + \
                self.project_name + "\""

            # Name of the test fixture itself
            self._fixture_name = \
                "\"pymake-internal-build-tests-fixture-" + \
                self.project_name + "\""

            with generator.open_method_block("add_test") as b:
                b.add_arguments(self._fixture_target_name)
                b.add_arguments('"${CMAKE_COMMAND}"')
                b.add_arguments('--build "${CMAKE_BINARY_DIR}"')
                b.add_arguments('--config $<CONFIG>')
                b.add_arguments(f"--target {self._project_test_target_name}")
            with generator.open_method_block("set_tests_properties") as b:
                b.add_arguments(self._fixture_target_name)
                b.add_arguments("PROPERTIES")
                b.add_keyword_arguments(
                    "FIXTURES_SETUP",
                    self._fixture_name
                )


    @property
    def project_name(self) -> str:
        """
        Gets the name of the project.
        """
        return self._project_name


    @property
    def project_languages(self) -> Iterable[EProjectLanguage]:
        """
        Gets the languages used in the project.
        """
        return self._project_languages


    def add_executable(self,
        target_name: str) -> ExecutableTarget:
        """
        Adds an executable target to the project.
        @param target_name Name of the target.
        @throws ValueError Thrown if a target with the given name already exists.
        @returns The target instance.
        """
        target = self._add_target(ExecutableTarget(
            self._build_scripts,
            target_name,
            self._project_all_target_name
        ))
        assert isinstance(target, ExecutableTarget)
        return target


    def add_gtest_target(self,
        target_name: str) -> GoogleTestTarget:
        """
        Adds a GoogleTest executable target to the project.
        The target will be added to the project's `test` target.
        @param target_name Name of the target.
        @throws ValueError Thrown if a target with the given name already exists.
        @throws RuntimeError Thrown if testing is not enabled for the project.
        @returns The target instance.
        """
        if not self._enable_ctest:
            raise RuntimeError(
                "Cannot add a GoogleTest target to a project that does not " +
                "have testing enabled."
            )

        target = self._add_target(GoogleTestTarget(
            self._build_scripts,
            target_name,
            self._project_all_target_name,
            self._project_test_target_name,
            self._fixture_name
        ))
        assert isinstance(target, GoogleTestTarget)
        self._test_targets[target_name] = target
        return target


    def add_static_library(self,
        target_name: str) -> StaticLibraryTarget:
        """
        Adds a static library target to the project.
        @param target_name Name of the target.
        @throws ValueError Thrown if a target with the given name already exists.
        @returns The target instance.
        """
        target = self._add_target(StaticLibraryTarget(
            self._build_scripts,
            target_name,
            self._project_all_target_name
        ))
        assert isinstance(target, StaticLibraryTarget)
        return target


    def add_shared_library(self,
        target_name: str) -> SharedLibraryTarget:
        """
        Adds a shared library target to the project.
        @param target_name Name of the target.
        @throws ValueError Thrown if a target with the given name already exists.
        @returns The target instance.
        """
        target = self._add_target(SharedLibraryTarget(
            self._build_scripts,
            target_name,
            self._project_all_target_name
        ))
        assert isinstance(target, SharedLibraryTarget)
        return target


    def _add_target(self, target: ITarget) -> ITarget:
        """
        Adds a target to the project.
        @param target Target to add.
        @throws ValueError Thrown if a target with the given name already
          exists and is defined at a different location.
        @returns The newly created target, or the previously added target if it
          was defined at the same location as the target being added.
        """
        # Check if a target with the given name already exists
        prev_target = self._check_is_target_redefined(target)
        if prev_target:
            return prev_target

        # Add the target to the project
        target.generate_declaration()
        self._targets[target.target_name] = target
        return target


    def _check_is_target_redefined(self,
        target: ITarget) -> Optional[ITarget]:
        """
        Checks if the given target is being redefined.
        @param target Target to check.
        @throws ValueError Thrown if the target is being redefined at a
          different location.
        @returns The previously added target if it was defined at the same
          location as the target being added, `None` otherwise. If a target
          is returned, the returned target is guaranteed to be the same type as
          `target`.
        """
        # Check if a target with the given name already exists
        prev_target = self._on_target_added(target)
        if prev_target:
            # If the previously added target is defined at the same location as
            #   the target being added, return the previously added target
            # This is necessary to allow build scripts to import targets from
            #   other build scripts while also allowing build scripts to contain
            #   code in the top-level scope.
            if prev_target.origin.file_path == target.origin.file_path and \
                prev_target.origin.line_number == target.origin.line_number:
                return prev_target

            error_str = "Error: A target with the name " + \
                f"'{target.target_name}' already exists.\n"
            error_str += "Note: The target was previously added at " + \
                f"{prev_target.origin.file_path}:" + \
                f"{prev_target.origin.line_number}\n"
            error_str += "Note: Target is being redefined at " + \
                f"{target.origin.file_path}:" + \
                f"{target.origin.line_number}"
            raise ValueError(error_str)

        return None


    def _set_on_target_added(self,
        callback: Callable[[ITarget], None]) -> None:
        """
        Sets the callback that will be invoked when a target is added.
        @param callback Callback to invoke when a target is added to the project.
        """
        self._on_target_added = callback


    # Allow external objects to bind to the `on_target_added` event
    on_target_added = property(fset=_set_on_target_added)
