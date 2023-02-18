from pathlib import Path
from pymake.generation.build_script import BuildScript
from pymake.helpers.caller_info import CallerInfo
from pymake.helpers.path_statics import shorten_path
from typing import Dict

class ProjectState:
    """
    Contains information about a CMake project created via PyMake.
    This class contains state information for a single CMake project and is
      intended to be shared between all PyMake objects that are part of the same
      CMake project.
    """
    # Name used for build scripts that are the equivalent of CMakeLists.txt.
    PRIMARY_BUILD_SCRIPT_NAME = "make.py"

    def __init__(self,
        source_tree_path: Path,
        generated_tree_path: Path):
        """
        Initializes the object.
        @param source_tree_path Path to the root of the PyMake project's source
          tree.
        @param generated_tree_path Path to folder where the PyMake project's
          generated CMake files should be written to.
        """
        self._source_tree_path = source_tree_path.absolute().resolve()
        self._generated_tree_path = generated_tree_path.absolute().resolve()

        # Each build script will be indexed under the relative path from the
        #   source tree to the build script, except for those located outside
        #   the source tree. Build scripts located outside the source tree will
        #   be indexed under their absolute path instead.
        self._build_scripts: Dict[Path, BuildScript] = {}

    @property
    def build_scripts(self) -> Dict[Path, BuildScript]:
        """
        Gets all build scripts for the project.
        @returns A dictionary of all build scripts for the project. Each build
          script will be indexed under the path to the build script. If the
          build script is in the source tree, this will be the relative path
          from the source tree path to the build script. Build scripts located
          outside the source tree will be indexed by their absolute path.
        """
        return self._build_scripts

    @property
    def generated_tree_path(self) -> Path:
        """
        Gets the path to the generated tree for the PyMake project.
        @returns The absolute path to the generated tree root. This path will
          not contain any symlinks.
        """
        return self._generated_tree_path

    @property
    def source_tree_path(self) -> Path:
        """
        Gets the path to the source tree for the PyMake project.
        @returns The absolute path to the source tree root. This path will not
          contain any symlinks.
        """
        return self._source_tree_path

    def get_or_add_build_script(self, caller_offset: int):
        """
        Gets the build script instance assigned to the current PyMake script.
        @param caller_offset Number of stack frames to traverse to get to
          the stack frame of the pymake build script's stack frame.
        """
        caller_info = CallerInfo(caller_offset + 1)
        build_script_rel_path = shorten_path(
            caller_info.file_path.parent,
            self._source_tree_path
        )

        # If the PyMake script already has a build script instance associated
        #   with it, return it. Otherwise, create a new build script instance
        #   for the PyMake script.
        if build_script_rel_path in self._build_scripts:
            return self._build_scripts[build_script_rel_path]
        else:
            build_script = BuildScript(
                self._get_target_build_script_name(caller_info.file_path.name),
                build_script_rel_path,
                self._generated_tree_path
            )
            self._build_scripts[build_script_rel_path] = build_script
            return build_script

    def _get_target_build_script_name(self, script_name: str) -> str:
        """
        Determines the name of the CMake build script to generate for the script.
        @param script_name Name of the PyMake build script that a CMake build
          script should be generated for. This must contain only the file name
          of the PyMake build script and should not contain any path information.
        @returns The name of the CMake file to generate for the build script.
          This will be a file name only and will not contain path information.
        """
        if script_name == ProjectState.PRIMARY_BUILD_SCRIPT_NAME:
            return "CMakeLists.txt"
        else:
            return script_name.replace(".py", ".cmake")
