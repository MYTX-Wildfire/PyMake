from pymake.common.project_language import EProjectLanguage
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
        @param project_name Name assigned to the project.
        """
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
