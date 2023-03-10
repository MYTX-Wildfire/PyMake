from pathlib import Path
from pymake.common.project_language import EProjectLanguage
from pymake.common.test_flags import ETestFlags
from pymake.core.build_script import BuildScript
from pymake.data.executable_target import ExecutableTarget
from pymake.data.library_set import LibrarySet
from pymake.generators.cmake_generator import CMakeGenerator
from pymake.tracing.traced import ITraced
from pymake.tracing.traced_dict import TracedDict
from typing import Iterable, List, Optional

class ProjectScope(ITraced):
    """
    Represents a project scope within a PyMake project.
    Project scopes are used to group related targets together. Each project
      scope will have an `all` target and a `test` target generated for it,
      which will build all targets in the project and run all tests targets
      in the project, respectively.
    """
    def __init__(self,
        project_name: str,
        project_languages: EProjectLanguage | Iterable[EProjectLanguage],
        project_all_target_name: Optional[str] = None,
        project_all_suffix: str = "-all",
        project_test_target_name: Optional[str] = None,
        project_test_suffix: str = "-test"):
        """
        Initializes the project scope.
        @param project_name The name of the project.
        @param project_languages The languages used in the project.
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
        self._project_name = project_name
        if isinstance(project_languages, EProjectLanguage):
            project_languages = [project_languages]
        self._project_languages = list(project_languages)

        # Determine the name to use for the project's `all` target
        if project_all_target_name is None:
            project_all_target_name = f"{project_name}{project_all_suffix}"
        self._project_all_target_name = project_all_target_name

        # Determine the name to use for the project's `test` target
        if project_test_target_name is None:
            project_test_target_name = f"{project_name}{project_test_suffix}"
        self._project_test_target_name = project_test_target_name

        # All target sets in the project
        self._target_sets: TracedDict[str, LibrarySet] = TracedDict()

        # All executables in the project
        self._executables: TracedDict[str, ExecutableTarget] = TracedDict()


    @property
    def project_name(self) -> str:
        """
        Gets the name of the project.
        """
        return self._project_name


    @property
    def project_languages(self) -> List[EProjectLanguage]:
        """
        Gets the languages used in the project.
        """
        return self._project_languages


    @property
    def project_all_target_name(self) -> str:
        """
        Gets the name of the project's `all` target.
        """
        return self._project_all_target_name


    @property
    def project_test_target_name(self) -> str:
        """
        Gets the name of the project's `test` target.
        """
        return self._project_test_target_name


    def add_executable(self,
        target_name: str,
        sanitizer_flags: int) -> ExecutableTarget:
        """
        Adds a new executable target.
        @param target_name The name of the target.
        @param sanitizer_flags The sanitizer flags to use for the target.
        @throws RuntimeError If an executable with the same name has already
          and was added from a different location.
        @throws RuntimeError If the target name has been used for a library
          set that was previously added.
        @returns The executable target. This will either be a previously added
          executable or a newly constructed target.
        """
        target = ExecutableTarget(
            target_name,
            ETestFlags.NONE,
            sanitizer_flags
        )

        # Check if a library set with the same name has already been added
        if target_name in self._target_sets:
            prev_lib_set = self._target_sets[target_name]
            error_str = "Error: Cannot add an executable with the name " + \
                f"'{target_name}' because a library set with that name " + \
                "already exists.\n"
            error_str += "Note: The library set was previously added at " + \
                f"{prev_lib_set.origin.file_path}:{prev_lib_set.origin.line_number}"
            error_str += "Note: The new executable is being added at " + \
                f"{target.origin.file_path}:{target.origin.line_number}"
            raise RuntimeError(error_str)

        # Check if an executable with the same name has already been added
        if target_name in self._executables:
            # If the previously added executable was added at the same location
            #   as the new executable, then return the previously added
            #   executable. Otherwise, raise an error.
            prev_exe = self._executables[target_name]
            if prev_exe.origin == target.origin:
                return prev_exe

            error_str = "Error: An executable with the name " + \
                f"'{target_name}' already exists.\n"
            error_str += "Note: The executable was previously added at " + \
                f"{prev_exe.origin.file_path}:" + \
                f"{prev_exe.origin.line_number}\n"
            error_str += "Note: The new executable is being added at " + \
                f"{target.origin.file_path}:" + \
                f"{target.origin.line_number}"
            raise RuntimeError(error_str)

        # Add the executable to the project
        self._executables[target_name] = target
        return target


    def add_library(self,
        target_set_name: str,
        common_target_name: Optional[str],
        common_target_suffix: str = "-common") -> LibrarySet:
        """
        Adds a new library set.
        @param target_set_name The name of the target set.
        @param common_target_name The name to use for the common target. If
          None, the common target name will be the target set name plus
          `common_target_suffix`.
        @param common_target_suffix The suffix to append to target set name if
          `common_target_name` is None.
        @throws RuntimeError If a library set with the same name has already
          and was added from a different location.
        @throws RuntimeError If the target set name has been used for an
          executable that was previously added.
        """
        library_set = LibrarySet(
            target_set_name,
            common_target_name,
            common_target_suffix
        )

        # Check if an executable with the same name has already been added
        if target_set_name in self._executables:
            prev_exe = self._executables[target_set_name]
            error_str = "Error: Cannot add a library set with the name " + \
                f"'{target_set_name}' because an executable with that name " + \
                "already exists.\n"
            error_str += "Note: The executable was previously added at " + \
                f"{prev_exe.origin.file_path}:" + \
                f"{prev_exe.origin.line_number}\n"
            error_str += "Note: The new library set is being added at " + \
                f"{library_set.origin.file_path}:" + \
                f"{library_set.origin.line_number}"
            raise RuntimeError(error_str)

        # Check if a library set with the same name has already been added
        if target_set_name in self._target_sets:
            # If the previously added library set was added at the same location
            #   as the new set, then return the previously added library set.
            #   Otherwise, raise an error.
            prev_set = self._target_sets[target_set_name]
            if prev_set.origin == library_set.origin:
                return prev_set

            error_str = "Error: A library set with the name " + \
                f"'{target_set_name}' already exists.\n"
            error_str += "Note: The library set was previously added at " + \
                f"{prev_set.origin.file_path}:" + \
                f"{prev_set.origin.line_number}\n"
            error_str += "Note: The new library set is being added at " + \
                f"{library_set.origin.file_path}:" + \
                f"{library_set.origin.line_number}"
            raise RuntimeError(error_str)

        # Add the new library set
        self._target_sets[target_set_name] = library_set
        return library_set


    def generate_project(self,
        project_dir: Path,
        build_script: BuildScript):
        """
        Generates the CMake code for the object.
        @param project_dir Path to the directory that all of the generated
          CMake files for the project should be placed in. This will be an
          absolute path to a directory.
        @param build_script The build script to write the CMake code to.
        """
        assert project_dir.is_absolute()
        assert project_dir.is_dir()
        generator = build_script.generator

        # Generate the project declaration
        with generator.open_method_block("project") as b:
            b.add_arguments(self._project_name)
            b.add_keyword_arguments(
                "LANGUAGES",
                *[l.value for l in self._project_languages]
            )

        # Enable CTest
        with generator.open_method_block("include") as b:
            b.add_arguments("CTest")
        with generator.open_method_block("enable_testing") as b:
            pass

        # Generate the project's `all` target
        with generator.open_method_block("add_custom_target") as b:
            b.add_arguments(self._project_all_target_name)
            # Since the project's 'all' target doesn't build anything directly,
            #   add it to the `ALL` build target for completeness
            b.add_arguments("ALL")

        # Generate the project's `test` target
        with generator.open_method_block("add_custom_target") as b:
            b.add_arguments(self._project_test_target_name)
            # Since the project's 'test' target doesn't build anything directly,
            #   add it to the `ALL` build target for completeness
            b.add_arguments("ALL")

        # Set up a fixture that forces CMake to build the test targets before
        #   running the tests
        # CMake's default behavior is to not build the test targets before
        #   trying to run them. This behavior has been reported as a bug in
        #   2009, but CMake has yet to introduce a (dedicated) workaround
        #   for this behavior:
        #   https://gitlab.kitware.com/cmake/cmake/-/issues/8774
        # To get around this, use CMake fixtures as mentioned here:
        #   https://stackoverflow.com/a/56448477

        # Name used for the target that the test fixture builds
        fixture_target_name = "\"pymake-internal-build-tests-fixture-target-" + \
            self._project_name + "\""

        # Name of the test fixture itself
        fixture_name = "\"pymake-internal-build-tests-fixture-" + \
            self._project_name + "\""

        with generator.open_method_block("add_test") as b:
            b.add_arguments(fixture_target_name)
            b.add_arguments('"${CMAKE_COMMAND}"')
            b.add_arguments('--build "${CMAKE_BINARY_DIR}"')
            b.add_arguments('--config $<CONFIG>')
            b.add_arguments(f"--target {self._project_test_target_name}")
        with generator.open_method_block("set_tests_properties") as b:
            b.add_arguments(fixture_target_name)
            b.add_arguments("PROPERTIES")
            b.add_keyword_arguments(
                "FIXTURES_SETUP",
                fixture_name
            )

        # Generate add_subdirectory() calls for all target sets and executables
        for set_name, _ in self._target_sets:
            with generator.open_method_block("add_subdirectory") as b:
                b.add_arguments(set_name)
        for exe_name, _ in self._executables:
            with generator.open_method_block("add_subdirectory") as b:
                b.add_arguments(exe_name)

        # Write the project's build script to disk
        build_script.write_file()

        # Generate build scripts for each target set in the project
        for set_name, target_set in self._target_sets:
            target_set_dir = project_dir / set_name
            target_set_dir.mkdir(parents=True, exist_ok=True)

            target_set_build_script = BuildScript(
                target_set_dir / "CMakeLists.txt",
                generator=CMakeGenerator(
                    formatter=generator.formatter,
                    use_spaces=generator.use_spaces,
                    tab_size=generator.tab_size
                )
            )
            target_set.generate_target_set(target_set_build_script)

        # Generate build scripts for each executable in the project
        for exe_name, exe in self._executables:
            exe_dir = project_dir / exe_name
            exe_dir.mkdir(parents=True, exist_ok=True)

            exe_build_script = BuildScript(
                exe_dir / "CMakeLists.txt",
                generator=CMakeGenerator(
                    formatter=generator.formatter,
                    use_spaces=generator.use_spaces,
                    tab_size=generator.tab_size
                )
            )
            exe.generate_target(exe_build_script)
