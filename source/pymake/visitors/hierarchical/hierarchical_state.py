from pymake.generators.build_script import BuildScript
from pymake.generators.cmake_generator import CMakeGenerator
from pymake.model.project_scope import ProjectScope
from pymake.model.pymake_project import PyMakeProject
from pymake.model.target_set import TargetSet
from pymake.model.targets.target import Target
from pymake.tracing.caller_info_formatter import ICallerInfoFormatter
from pymake.tracing.shortened_caller_info_formatter import ShortenedCallerInfoFormatter
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

class HierarchicalState:
    """
    Stores state information for hierarchical visitors.
    """
    def __init__(self,
        project: PyMakeProject,
        formatter: Optional[ICallerInfoFormatter] = None,
        use_spaces: bool = False,
        indent_size: int = 4):
        """
        Initializes the object for the project.
        @param project Project that the state information is being gathered for.
        @param formatter Formatter to use to format caller information. If
          None, a default formatter will be used.
        @param use_spaces True if spaces should be used for indentation, False
          if tabs should be used.
        @param indent_size Number of spaces or tabs to use for each level of
          indentation. Only used if use_spaces is True.
        """
        self._project = project
        self._formatter = formatter or ShortenedCallerInfoFormatter(
            project.source_dir
        )
        self._use_spaces = use_spaces
        self._indent_size = indent_size

        ## Build scripts for each node in the project.
        # Each script will be indexed by the node that it is for. Build scripts
        #   are created for the project, all project scopes, all target sets,
        #   and all targets within each target set.
        self._build_scripts: Dict[Any, BuildScript] = {}

        ## Maps project names to their build paths.
        # Each path will be an absolute path that is located within the
        #   project's build directory.
        self._target_build_paths: Dict[str, Path] = {}

        ## Maps each target set to the project scope that owns it.
        # Each target set is stored by its set name.
        self._target_set_parents: Dict[str, ProjectScope] = {}

        ## Maps each target to the target set that owns it.
        # Each target is stored by its target name.
        self._target_parents: Dict[str, TargetSet] = {}

        ## Keep track of all test targets in the project.
        self._test_targets: List[Target] = []

        # Initialize the state variables
        self._process_project(self._project)


    @property
    def test_targets(self) -> List[Target]:
        """
        Gets all test targets in the project.
        """
        return self._test_targets


    def generate_build_scripts(self):
        """
        Generates the build scripts for the project.
        """
        # A build script may appear more than once in the `_build_scripts`
        #   dictionary because a target's build script is the same as its
        #   target set's build script. Keep track of which paths have already
        #   been generated so that each build script is only generated once.
        generated_paths: Set[Path] = set()
        for build_script in self._build_scripts.values():
            if build_script.target_path not in generated_paths:
                build_script.write_file()
                generated_paths.add(build_script.target_path)


    def get_build_script_for_node(self, node: Any) -> BuildScript:
        """
        Gets the build script for the given node.
        @param node Node to get the build script for.
        @returns The build script for the given node.
        """
        assert node in self._build_scripts
        return self._build_scripts[node]


    def get_target_build_path(self, target: str | Target) -> Path:
        """
        Gets the path within the generated build directory where the target's
            build file will be generated.
        @param target Target name or target object to get the build path for.
        @return Path within the generated build directory where the target's
            build file will be generated. This will be an absolute path to a
            file.
        """
        if isinstance(target, Target):
            target = target.target_name
        return self._target_build_paths[target]


    def get_test_fixture_target_name(self, project: ProjectScope) -> str:
        """
        Gets the target name used for the project's test fixture.
        @remarks A test fixture is used to force CMake to build test executables
          before attempting to run tests. For more information, see here:
          https://stackoverflow.com/a/56448477
        @param project Project to get the test fixture target name for.
        @returns The target name of the test fixture for the project.
        """
        return "pymake-internal-build-tests-fixture-target-" + \
            project.project_name


    def get_test_fixture_name(self, project: ProjectScope | Target) -> str:
        """
        Gets the name of the test fixture for the project or target.
        @remarks See `get_test_fixture_target_name` for more information.
        @param project Project or target to get the test fixture name for.
        @returns The name of the test fixture for the project or target.
        """
        if isinstance(project, Target):
            # "Rename" the parameter to make it clear that it's a target
            target = project

            # Look up the target set that owns the target, then get the project
            #   scope for the target set
            assert target.target_name in self._target_parents
            target_set = self._target_parents[target.target_name]
            assert target_set.set_name in self._target_set_parents
            project = self._target_set_parents[target_set.set_name]
            return self.get_test_fixture_target_name(project)
        else:
            return f"pymake-internal-build-tests-fixture-{project.project_name}"


    def _create_cmake_generator(self) -> CMakeGenerator:
        """
        Creates a CMake generator to use for generating build scripts.
        @returns A CMake generator to use for generating build scripts.
        """
        return CMakeGenerator(
            self._formatter,
            self._use_spaces,
            self._indent_size
        )


    def _process_project(self, project: PyMakeProject):
        """
        Updates internal state for the given project.
        @param project Project to process and update internal state for.
        """
        # Create the build script for the project
        project_build_script_path = project.generated_dir / "CMakeLists.txt"
        project_build_script = BuildScript(
            project_build_script_path,
            self._create_cmake_generator()
        )
        assert project not in self._build_scripts
        self._build_scripts[project] = project_build_script

        # Populate the reverse lookup dictionaries
        for scope in project.project_scopes:
            self._process_project_scope(project, scope)


    def _process_project_scope(self,
        project: PyMakeProject,
        scope: ProjectScope):
        """
        Updates internal state for the given project scope.
        @param project Project that owns the scope.
        @param scope Project scope to process and update internal state for.
        """
        # Create the build script for the target set
        project_scope_build_script_path = project.generated_dir
        project_scope_build_script_path /= scope.project_name
        project_scope_build_script_path /= "CMakeLists.txt"
        project_scope_build_script = BuildScript(
            project_scope_build_script_path,
            self._create_cmake_generator()
        )
        assert scope not in self._build_scripts
        self._build_scripts[scope] = project_scope_build_script

        for target_set in scope.target_sets:
            self._process_target_set(project, scope, target_set)


    def _process_target_set(self,
        project: PyMakeProject,
        scope: ProjectScope,
        target_set: TargetSet):
        """
        Updates internal state for the given target set.
        @param project Project that owns the target set.
        @param scope Project scope that owns the target set.
        @param target_set Target set to process and update internal state for.
        """
        # Map each target set back to its parent scope
        assert target_set.set_name not in self._target_set_parents
        self._target_set_parents[target_set.set_name] = scope

        # Create the build script for the target set
        target_set_build_script_path = project.generated_dir
        target_set_build_script_path /= scope.project_name
        target_set_build_script_path /= target_set.set_name
        target_set_build_script_path /= "CMakeLists.txt"
        target_set_build_script = BuildScript(
            target_set_build_script_path,
            self._create_cmake_generator()
        )
        assert target_set not in self._build_scripts
        self._build_scripts[target_set] = target_set_build_script

        for target in target_set.targets:
            self._process_target(project, scope, target_set, target)


    def _process_target(self,
        project: PyMakeProject,
        scope: ProjectScope,
        target_set: TargetSet,
        target: Target):
        """
        Updates internal state for the given target.
        @param project Project that owns the target.
        @param scope Project scope that owns the target.
        @param target_set Target set that owns the target.
        @param target Target to process and update internal state for.
        """
        # Map each target back to its target set
        assert target.target_name not in self._target_parents
        self._target_parents[target.target_name] = target_set

        # Store the path within the generated build directory where
        #   the target's build file will be generated
        assert target.target_name not in self._target_build_paths
        target_binary_path = project.build_dir
        target_binary_path /= scope.project_name
        target_binary_path /= target_set.set_name
        # TODO: Get the target's file name using the target's
        #   properties rather than assuming it's the same as the
        #   target's name
        target_binary_path /= target.target_name
        self._target_build_paths[target.target_name] = \
            target_binary_path

        # Create the build script for the target
        target_build_script_path = project.generated_dir
        target_build_script_path /= scope.project_name
        target_build_script_path /= target_set.set_name
        target_build_script_path /= target.target_name
        target_build_script_path /= "CMakeLists.txt"
        target_build_script = BuildScript(
            target_build_script_path,
            self._create_cmake_generator()
        )
        assert target not in self._build_scripts
        self._build_scripts[target] = target_build_script

        # Keep track of all test targets
        if target.is_test:
            self._test_targets.append(target)
