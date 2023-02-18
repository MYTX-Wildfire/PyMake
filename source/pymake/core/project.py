from pymake.common.project_language import EProjectLanguage
from pymake.generation.basic_generator import BasicGenerator
from pymake.generation.build_script import BuildScript
from pymake.helpers.caller_info import CallerInfo
from typing import Iterable

class Project:
    """
    Represents a CMake project scope.
    """
    def __init__(self,
        build_script: BuildScript,
        project_name: str,
        project_languages: EProjectLanguage | Iterable[EProjectLanguage]):
        """
        Initializes the object.
        @param build_script Build script to write CMake code to.
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
        # Instances of this class are constructed via calls to `CMake` class
        #   methods, so the actual call site this class should capture is 3
        #   levels up (CallerInfo frame (0) => This constructor's frame (1) =>
        #   the CMake class's method's frame (2) => the target call site (3)).
        self._call_site = CallerInfo(3)
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

        build_script.add_generator(BasicGenerator(
            code,
            # This class is always instantiated via a `CMake` object, so the
            #   PyMake build script's stack frame will be two levels up from
            #   the current stack frame
            caller_offset=2
        ))
