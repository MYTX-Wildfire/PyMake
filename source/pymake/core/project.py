from pymake.common.project_language import EProjectLanguage
from pymake.core.executable_target import ExecutableTarget
from pymake.core.project_state import ProjectState
from pymake.core.target import Target
from pymake.generation.basic_generator import BasicGenerator
from pymake.tracing.caller_info import CallerInfo
from pymake.helpers.code_generator import CodeGenerator
import sys
from typing import Iterable, Dict

class Project:
    """
    Represents a CMake project scope.
    """
    def __init__(self,
        project_state: ProjectState,
        project_name: str,
        project_languages: EProjectLanguage | Iterable[EProjectLanguage]):
        """
        Initializes the object.
        @param project_state State object for the CMake project this object is
          part of.
        @param project_name Name to assign to the project. Must not be an empty
          string or all whitespace.
        @param project_languages Languages used by the project. At least one
          language must be specified.
        @throws ValueError thrown if any parameter is invalid.
        """
        # Validate method arguments
        if not project_name:
            raise ValueError("A project name string may not be empty.")
        elif project_name.isspace():
            raise ValueError("A project's name cannot be only whitespace.")
        if (not isinstance(project_languages, EProjectLanguage) and
            not project_languages):
            raise ValueError("At least one project language must be specified.")

        # Initialize member variables
        self._project_name = project_name
        self._project_state = project_state
        # Dictionary of targets in the project, indexed by target name
        self._targets: Dict[str, Target] = {}
        self._call_site = CallerInfo.closest_external_frame()
        if isinstance(project_languages, EProjectLanguage):
            self._project_languages = [project_languages]
        else:
            self._project_languages = list(project_languages)

        # Generate the CMake code for adding the project
        generator = CodeGenerator()
        generator.open_method("project")
        generator.write_method_parameter(None, project_name)
        generator.write_method_parameter(
            "LANGUAGES",
            [x.to_cmake_language() for x in self._project_languages]
        )
        generator.close_method()

        # Add the generated code to the build script
        build_script = project_state.get_or_add_build_script()
        build_script.add_generator(BasicGenerator(
            generator.code
        ))

    def add_executable(self, target_name: str) -> ExecutableTarget:
        """
        Adds an executable target to the project.
        @param target_name Name of the target to create.
        @throws ValueError Thrown if a target already exists with the given name.
        """
        # Validate the target name
        call_site = CallerInfo(1)
        prev_call_site = self._project_state.try_get_target(target_name)
        if prev_call_site:
            print(f"Cannot add target '{target_name}' defined at " +
                f"'{call_site.file_path}:{call_site.line_number}'",
                file=sys.stderr
            )
            print(f"A target with the same name was previously added at " +
                f"'{prev_call_site.file_path}:{prev_call_site.line_number}'",
                file=sys.stderr
            )
            raise ValueError(
                f"A target with the name '{target_name}' was already added."
            )

        # Create the target
        target = ExecutableTarget(
            self._project_state,
            target_name,
            caller_offset=1
        )
        self._targets[target_name] = target
        self._project_state.register_target(target_name, call_site)

        return target
