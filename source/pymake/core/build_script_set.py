import os
from pathlib import Path
from pymake.core.build_script import BuildScript
from pymake.generators.cmake_generator import CMakeGenerator
from pymake.tracing.caller_info import CallerInfo
from pymake.tracing.caller_info_formatter import ICallerInfoFormatter
from typing import Dict, Optional

class BuildScriptSet:
    """
    Stores all build script instances that must be generated.
    """
    # Path for external build scripts' generated files
    # This path is relative to the generated directory's path.
    EXTERNAL_GENERATED_DIR = ".external"

    def __init__(self,
        source_directory: Path,
        generated_directory: Path,
        formatter: ICallerInfoFormatter):
        """
        Initializes the set.
        @param source_directory Path to the directory containing the source
            files for the PyMake project. Must be an absolute path.
        @param generated_directory Path to the directory where PyMake should
          generate the CMake files. Must be an absolute path.
        @param formatter Formatter that should be used when printing tracing
          info.
        """
        assert source_directory.is_absolute()
        assert generated_directory.is_absolute()

        self._source_dir = source_directory
        self._generated_dir = generated_directory
        self._external_generated_dir = generated_directory / \
            BuildScriptSet.EXTERNAL_GENERATED_DIR
        self._formatter = formatter

        # Build scripts added to the project, indexed by the path of the PyMake
        #   build script that triggered the creation of the build script.
        # Each build script path will be an absolute path.
        self._build_scripts: Dict[Path, BuildScript] = {}


    def __bool__(self) -> bool:
        """
        Gets whether the set contains any build scripts.
        """
        return bool(self._build_scripts)


    def __len__(self) -> int:
        """
        Gets the number of build scripts in the set.
        """
        return len(self._build_scripts)


    def get_or_add_build_script(self, caller_path: Optional[Path] = None) \
        -> BuildScript:
        """
        Gets the build script for the specified PyMake build script.
        If a build script instance does not exist for the caller path, a build
          script instance will be created and added to the set.
        @param caller_path Path to the PyMake build script that triggered the
          creation of the build script. If this is None, the caller path will
          be determined using the closest external frame.
        """
        if caller_path is None:
            caller_path = CallerInfo.closest_external_frame().file_path
        assert caller_path.is_absolute()

        # If a build script already exists for the file, return it
        if caller_path in self._build_scripts:
            return self._build_scripts[caller_path]

        # A new build instance must be created. Figure out what path to use
        #   for the build script.
        try:
            rel_path = caller_path.relative_to(self._source_dir).parent
            target_path = self._generated_dir / rel_path
        except ValueError:
            # The build script lies outside of the source directory.
            # Use the path of the build script relative to the file system root
            #   as the path for the generated build script.
            fs_root = os.path.abspath('.').split(os.path.sep)[0] + os.path.sep
            rel_path = caller_path.relative_to(Path(fs_root)).parent
            target_path = self._external_generated_dir / rel_path

        generated_file_name = \
            BuildScriptSet.get_generated_build_script_name(caller_path)
        target_path /= generated_file_name

        # Create a new build script instance
        build_script = BuildScript(
            target_path,
            CMakeGenerator(self._formatter)
        )
        self._build_scripts[caller_path] = build_script
        return build_script


    def generate(self):
        """
        Generates all build scripts.
        """
        for build_script in self._build_scripts.values():
            print(f"Generating '{build_script.target_path}'...")
            build_script.generator.write_file(build_script.target_path)


    @staticmethod
    def get_generated_build_script_name(build_script_path: Path) -> str:
        """
        Gets the name to use for the generated build script.
        @param build_script_path Path to the PyMake build script that the build
          script is for.
        @return Name to use for the build script generated for the PyMake build
          script.
        """
        file_name = build_script_path.name

        # Translate `make.py` files as `CMakeLists.txt`
        if file_name == "make.py":
            return "CMakeLists.txt"
        else:
            # Replace the ".py" extension with ".cmake"
            return file_name[:-3] + ".cmake"
