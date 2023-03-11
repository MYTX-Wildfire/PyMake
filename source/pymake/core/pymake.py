from pathlib import Path
from pymake.common.cmake_version import ECMakeVersion
from pymake.model.pymake_project import PyMakeProject
from pymake.views.project_view import ProjectView

class PyMake:
    """
    Defines static methods for managing PyMake projects.
    """
    @staticmethod
    def create_project(
        cmake_version: ECMakeVersion,
        source_dir: str | Path = ".",
        generated_dir: str | Path = ".pymake",
        build_dir: str | Path = "_build",
        install_dir: str | Path = "_out") -> ProjectView:
        """
        Creates a new PyMake project.
        @param cmake_version The version of CMake to target when generating the
          project.
        @param source_dir The path to the folder containing all source files. If
          this is a relative path, it will be resolved relative to the caller's
          directory.
        @param generated_dir The path to the folder where PyMake will generate
          CMake files in.
        @param build_dir The path to the folder that CMake will use as its build
          tree.
        @param install_dir The path to the folder that CMake will use as its
          install tree.
        @return The newly created project.
        """
        return ProjectView(PyMakeProject.get_pymake_project_by_origin(
            cmake_version,
            source_dir,
            generated_dir,
            build_dir,
            install_dir
        ))