from pymake.common.project_language import EProjectLanguage
from pymake.core.project_state import ProjectState
from pymake.generation.basic_generator import BasicGenerator
from pymake.helpers.caller_info import CallerInfo
from typing import Iterable

class Project:
    """
    Represents a CMake project scope.
    """
    def __init__(self,
        project_state: ProjectState,
        project_name: str,
        project_languages: EProjectLanguage | Iterable[EProjectLanguage],
        caller_offset: int):
        """
        Initializes the object.
        @param project_state State object for the CMake project this object is
          part of.
        @param project_name Name to assign to the project. Must not be an empty
          string or all whitespace.
        @param project_languages Languages used by the project. At least one
          language must be specified.
        @param caller_offset Number of stack frames to traverse to get to
          the stack frame of the pymake build script.
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
        # Add 1 to the provided caller offset to account for this constructor's
        #   stack frame
        self._call_site = CallerInfo(caller_offset + 1)
        if isinstance(project_languages, EProjectLanguage):
            self._project_languages = [project_languages]
        else:
            self._project_languages = list(project_languages)

        # Add the equivalent CMake code
        code = f"project({project_name}\n"
        code += "\tLANGUAGES\n"
        for language in self._project_languages:
            code += f"\t\t{language.to_cmake_language()}\n"
        code += ")"

        build_script = project_state.get_or_add_build_script(caller_offset + 1)
        build_script.add_generator(BasicGenerator(
            code,
            caller_offset + 1
        ))
