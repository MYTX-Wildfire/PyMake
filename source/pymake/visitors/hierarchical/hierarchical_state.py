from pymake.core.build_script import BuildScript
from pymake.generators.cmake_generator import CMakeGenerator
from pymake.model.project_scope import ProjectScope
from pymake.model.pymake_project import PyMakeProject
from pymake.model.target_sets.target_set import ITargetSet
from pymake.model.targets.target import Target
from pymake.tracing.caller_info_formatter import ICallerInfoFormatter
from pymake.tracing.shortened_caller_info_formatter import ShortenedCallerInfoFormatter
from pathlib import Path
from typing import Any, Dict, Optional, Set

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
        formatter = formatter or ShortenedCallerInfoFormatter(
            project.source_dir
        )

        ## Build scripts for each node in the project.
        # Each script will be indexed by the node that it is for. Build scripts
        #   are only created for the project, all project scopes, and all target
        #   scopes. Each target will have an entry in this dictionary, but will
        #   map to the build script for the target's target set instead of
        #   having its own build script.
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
        self._target_set_owners: Dict[str, ITargetSet] = {}

        # Create the build script for the project
        project_build_script_path = project.generated_dir / "CMakeLists.txt"
        project_build_script = BuildScript(
            project_build_script_path,
            CMakeGenerator(
                formatter,
                use_spaces,
                indent_size
            )
        )
        assert project not in self._build_scripts
        self._build_scripts[project] = project_build_script

        # Populate the reverse lookup dictionaries
        for scope in project.project_scopes:
            # Create the build script for the target set
            project_scope_build_script_path = project.generated_dir
            project_scope_build_script_path /= scope.project_name
            project_scope_build_script = BuildScript(
                project_scope_build_script_path,
                CMakeGenerator(
                    formatter,
                    use_spaces,
                    indent_size
                )
            )
            assert scope not in self._build_scripts
            self._build_scripts[scope] = project_scope_build_script

            for target_set in scope.target_sets:
                # Map each target set back to its parent scope
                assert target_set.set_name not in self._target_set_parents
                self._target_set_parents[target_set.set_name] = scope

                # Create the build script for the target set
                target_set_build_script_path = project.generated_dir
                target_set_build_script_path /= scope.project_name
                target_set_build_script_path /= target_set.set_name
                target_set_build_script = BuildScript(
                    target_set_build_script_path,
                    CMakeGenerator(
                        formatter,
                        use_spaces,
                        indent_size
                    )
                )
                assert target_set not in self._build_scripts
                self._build_scripts[target_set] = target_set_build_script

                for target in target_set.targets:
                    # Map each target back to its target set
                    assert target.target_name not in self._target_set_owners
                    self._target_set_owners[target.target_name] = target_set

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

                    # Use the target set's build script for the target
                    assert target not in self._build_scripts
                    self._build_scripts[target] = target_set_build_script


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
