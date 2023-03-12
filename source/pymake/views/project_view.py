import argparse
from pymake.common.pymake_args import PyMakeArgs
from pymake.cmake.cmake import ICMake
from pymake.cmake.cmake314 import CMake314
from pymake.cmake.cmake325 import CMake325
from pymake.common.cmake_version import ECMakeVersion
from pymake.common.project_language import EProjectLanguage
from pymake.model.preset import Preset
from pymake.model.pymake_project import PyMakeProject
from pymake.views.project_scope_view import ProjectScopeView
from pymake.visitors.crawlers.project_crawler import IProjectCrawler
from pymake.visitors.crawlers.breadth_first_crawler import BreadthFirstCrawler
from pymake.visitors.hierarchical.hierarchical_visitor_set \
    import HierarchicalVisitorSet
from pymake.visitors.visitor_set import IVisitorSet
import sys
from typing import List, Iterable, Optional

class ProjectView:
    """
    Provides an interface for modifying a PyMake project.
    """
    def __init__(self, project: PyMakeProject):
        """
        Initializes the project view.
        @param project The project to provide a view for.
        """
        self._project = project

        # Construct a CMake instance for the project's target CMake version
        cmake_versions = {
            ECMakeVersion.V3_14: CMake314,
            ECMakeVersion.V3_25: CMake325
        }
        self._cmake: ICMake = cmake_versions[project.cmake_version]()


    def add_preset(self,
        preset_name: str,
        base_presets: Preset | Iterable[Preset] | None = None) -> Preset:
        """
        Adds a new preset to the project.
        @param preset_name The name of the preset.
        @param base_presets The presets that the new preset should inherit
          from.
        @returns The new preset.
        """
        if isinstance(base_presets, Preset):
            base_presets = [base_presets]
        elif not base_presets:
            base_presets = []

        preset = self._project.add_preset(preset_name)
        for base_preset in base_presets:
            preset.inherit_from(base_preset)
        return preset


    def build(self,
        args: Optional[Iterable[str]] = None,
        generate_first: bool = True,
        visitor_set: Optional[IVisitorSet] = None,
        crawler: Optional[IProjectCrawler] = None) -> int:
        """
        Builds the project.
        @param generate_first Whether to generate the project before building.
        @param visitor_set The visitor set to use when building the project.
          If `None`, a default visitor set will be used. Only used if
          `generate_first` is `True`.
        @param crawler The project crawler to use when building the project.
          If `None`, a default project crawler will be used. Only used if
          `generate_first` is `True`.
        @returns The exit code of the build process.
        """
        if args:
            args = list(args)
        else:
            args = sys.argv[1:]

        # Process command line arguments
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-v",
            "--verbose",
            action="store_true",
            help="Enables verbose output from CMake."
        )
        parser.add_argument(
            "presets",
            nargs="*",
            help="PyMake preset(s) to use when building the project."
        )
        cli_args = parser.parse_known_args(
            args,
            namespace=PyMakeArgs(
                verbose=False,
                presets=[]
            )
        )[0]
        assert isinstance(cli_args, PyMakeArgs)

        # Generate the project if necessary
        if generate_first:
            self.generate(visitor_set, crawler)

        # Get the preset(s) to use
        selected_presets: List[Preset] = []
        project_presets = {
            preset.preset_name: preset for preset in self._project.presets
        }

        for preset_name in cli_args.presets:
            if preset_name not in project_presets:
                raise ValueError(f"Error: Unknown preset '{preset_name}'")
            selected_presets.append(project_presets[preset_name])
        if not selected_presets:
            selected_presets = list(self._project.default_presets)
        if not selected_presets:
            raise ValueError("Error: No presets were specified")

        # Run the configure step
        configure_exit_code = self._cmake.configure(
            self._project,
            selected_presets
        )
        if configure_exit_code != 0:
            return configure_exit_code

        # Run the build step
        return self._cmake.build(self._project, selected_presets)


    def create_project_scope(self,
        project_name: str,
        project_languages: EProjectLanguage | Iterable[EProjectLanguage],
        project_all_target_name: Optional[str] = None,
        project_all_suffix: str = "-all",
        project_test_target_name: Optional[str] = None,
        project_test_suffix: str = "-test") -> ProjectScopeView:
        """
        Creates a new project scope.
        @param project_name The name of the project.
        @param project_languages The languages used in the project.
        @param enable_ctest Whether to enable CTest for the project.
        @param project_all_target_name Name of the project-specific `all`
          target. If `None`, the project's `all` target will be named
          `[project_name][project_all_suffix]`.
        @param project_all_suffix Suffix to append to the project name to
          generate the project's `all` target name. Only used if
          `project_all_target_name` is `None`.
        @param project_test_target_name Name of the project-specific `test`
          target. If `None`, the project's `test` target will be named
          `[project_name][project_test_suffix]`.
        @param project_test_suffix Suffix to append to the project name to
          generate the project's `test` target name. Only used if
          `project_test_target_name` is `None`.
        @throws RuntimeError Thrown if the project scope already exists with the
          same name and was declared at a different location.
        @return The view for the project scope.
        """
        # Determine the project's `all` target name.
        if project_all_target_name is None:
            project_all_target_name = f"{project_name}{project_all_suffix}"

        # Determine the project's `test` target name.
        if project_test_target_name is None:
            project_test_target_name = f"{project_name}{project_test_suffix}"

        return ProjectScopeView(
            self._project,
            self._project.add_project_scope(
                project_name,
                project_languages,
                project_all_target_name,
                project_test_target_name
            )
        )


    def generate(self,
        visitor_set: Optional[IVisitorSet] = None,
        crawler: Optional[IProjectCrawler] = None):
        """
        Generates the project's build files.
        @param visitor_set The visitor set that determines how build files are
          generated. If `None`, a default visitor set will be used.
        @param crawler The project crawler that determines the order that build
          files are processed and generated. If `None`, a default crawler will
          be used.
        """
        # If no visitor set was provided, use the default visitor set.
        if not visitor_set:
            visitor_set = HierarchicalVisitorSet(self._project)

        # If no crawler was provided, use the default crawler.
        if not crawler:
            crawler = BreadthFirstCrawler()

        # Generate the project's build files.
        crawler.crawl(self._project, visitor_set)


    def set_default_presets(self,
        presets: Preset | Iterable[Preset]) -> None:
        """
        Sets the default preset(s) for the project.
        @param presets The default preset(s) for the project.
        """
        self._project.set_default_presets(presets)
