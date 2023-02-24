from pathlib import Path
import subprocess
import shutil
from typing import List, Optional

class PyMakeHelpers:
    """
    Defines helper methods for managing a pymake project used by test cases.
    """
    def __init__(self,
        project_dir: str | Path,
        build_dir: str = "_build",
        install_dir: str = "_out",
        pymake_dir: str = ".pymake"):
        """
        Initializes the helper.
        @param project_dir Path to the directory containing the PyMake project.
          Can be a relative or absolute path. If the path is a relative path, it
          will be interpreted relative to the current working directory.
        @param build_dir Name of the build directory used by the project. This
          is expected to be a path relative to the project directory.
        @param install_dir Name of the install directory used by the project.
          This is expected to be a path relative to the project directory.
        @param pymake_dir Name of the directory that PyMake writes its generated
            CMake files to. This is expected to be a path relative to the
            project directory.
        """
        project_dir = Path(project_dir)
        if not project_dir.is_absolute():
            project_dir = Path.cwd() / project_dir

        # Make sure the path is to a folder that's a PyMake project
        if not (project_dir / "make.py").exists():
            raise ValueError("The specified path is not a PyMake project")

        self._project_dir = Path(project_dir)
        self._build_dir = self._project_dir / build_dir
        self._install_dir = self._project_dir / install_dir
        self._pymake_dir = self._project_dir / pymake_dir


    def build(self,
        presets: str | List[str],
        flags: str | List[str] | None = None) -> int:
        """
        Builds the project.
        @param presets Name of the preset to use when building the project. Each
          entry must be a preset supported by the project.
        @param flags Additional flags to pass to the build command.
        @return The exit code of the build process.
        """
        if isinstance(presets, str):
            presets = [presets]
        if isinstance(flags, str):
            flags = [flags]
        elif flags is None:
            flags = []

        # Run the build command
        process = subprocess.run(
            ["python3", "make.py"] + presets + flags,
            cwd=self._project_dir,
            check=False
        )
        return process.returncode


    def clean(self):
        """
        Delete all project files.
        """
        if self._build_dir.exists():
            shutil.rmtree(self._build_dir)
        if self._install_dir.exists():
            shutil.rmtree(self._install_dir)
        if self._pymake_dir.exists():
            shutil.rmtree(self._pymake_dir)


    def find_generated_file(self,
        file_name: str,
        output_path: Optional[str] = None) -> bool:
        """
        Finds a file in the project's generated directory.
        @param file_name Name of the file to find.
        @param output_path Path to the directory where the file should be found.
            Must be a path relative to the generated directory if provided. Can be
            a path to a file or folder. If the path is to a folder, only that
            folder will be searched for a file with the target name. If not
            provided, the entire generated directory will be searched.
        @return Whether a file with the name was found.
        """
        return self._find_file(self._pymake_dir, file_name, output_path)


    def find_installed_file(self,
        file_name: str,
        output_path: Optional[str] = None) -> bool:
        """
        Finds a file in the project's install directory.
        @param file_name Name of the file to find.
        @param output_path Path to the directory where the file should be found.
          Must be a path relative to the install directory if provided. Can be
          a path to a file or folder. If the path is to a folder, only that
          folder will be searched for a file with the target name. If not
          provided, the entire install directory will be searched.
        @return Whether a file with the name was found.
        """
        return self._find_file(self._install_dir, file_name, output_path)


    def _find_file(self,
        search_dir: Path,
        file_name: str,
        output_path: Optional[str] = None) -> bool:
        """
        Finds a file in the specified directory.
        @param search_dir Directory to search.
        @param file_name Name of the file to find.
        @param output_path Path to the directory where the file should be found.
            Must be a path relative to the install directory if provided. Can be
            a path to a file or folder. If the path is to a folder, only that
            folder will be searched for a file with the target name. If not
            provided, the entire install directory will be searched.
        @return Whether a file with the name was found.
        """
        # Determine which directory should be searched
        if output_path:
            search_dir = search_dir / output_path

        # `output_path` can be a path to a file or folder. If it's a path to a
        #   folder, only search that folder. If the path is to a file, simply
        #   check if a file exists at that path.
        if not search_dir.is_dir():
            return search_dir.exists()

        # Search the directory for the file
        for _ in search_dir.rglob(file_name):
            return True
        return False
