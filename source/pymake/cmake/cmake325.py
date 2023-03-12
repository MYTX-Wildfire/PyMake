from pymake.cmake.cmake import ICMake
from pymake.model.pymake_project import PyMakeProject
from pymake.model.preset import Preset
import subprocess
from typing import List

class CMake325(ICMake):
    """
    Class for handling CMake 3.25 behavior.
    """
    def configure(self,
        project: PyMakeProject,
        presets: List[Preset]) -> int:
        """
        Runs the CMake configure step on the project.
        @param project The project to configure.
        @param presets The preset(s) to configure CMake to use. Must contain at
          least one element.
        @return The exit code of the CMake configure step.
        """
        assert presets

        # Build the CMake command to invoke
        cmake_cmd = [ "cmake3.25" ]
        for preset in presets:
            cmake_cmd.append("--preset")
            cmake_cmd.append(preset.preset_name)

        # Invoke CMake
        print("Running command: " + " ".join(cmake_cmd))
        return subprocess.run(
            cmake_cmd,
            cwd=project.generated_dir
        ).returncode


    def build(self,
        project: PyMakeProject,
        presets: List[Preset]) -> int:
        """
        Runs the CMake build step on the project.
        @param project The project to build.
        @param presets The preset(s) to build. Must contain at least one element.
        @return The exit code of the CMake build step.
        """
        assert presets

        # Build the CMake command to invoke
        cmake_cmd = [ "cmake3.25", "--build" ]
        for preset in presets:
            cmake_cmd.append("--preset")
            cmake_cmd.append(preset.preset_name)

        # Invoke CMake
        print("Running command: " + " ".join(cmake_cmd))
        return subprocess.run(
            cmake_cmd,
            cwd=project.generated_dir
        ).returncode
