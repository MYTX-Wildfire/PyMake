from pymake.common.project_language import EProjectLanguage
from pymake.model.target_set import TargetSet
from pymake.tracing.traced import ITraced
from pymake.tracing.traced_dict import TracedDict
from typing import Iterable, List

class ProjectScope(ITraced):
    """
    Represents a project scope within a PyMake project.
    Project scopes are used to group related targets together. Each project
      scope will have an `all` target and a `test` target generated for it,
      which will build all targets in the project and run all tests targets
      in the project, respectively.
    """
    def __init__(self,
        project_name: str,
        project_languages: EProjectLanguage | Iterable[EProjectLanguage],
        project_all_target_name: str,
        project_test_target_name: str):
        """
        Initializes the project scope.
        @param project_name The name of the project.
        @param project_languages The languages used in the project.
        @param enable_ctest Whether to enable CTest for the project.
        @param project_all_target_name Name of the project-specific `all`
          target.
        @param project_test_target_name Name of the project-specific `test`
          target.
        """
        super().__init__()

        self._project_name = project_name
        if isinstance(project_languages, EProjectLanguage):
            project_languages = [project_languages]
        self._project_languages = list(project_languages)
        self._project_all_target_name = project_all_target_name
        self._project_test_target_name = project_test_target_name

        # All target sets in the project
        self._target_sets: TracedDict[str, TargetSet] = TracedDict()


    @property
    def project_name(self) -> str:
        """
        Gets the name of the project.
        """
        return self._project_name


    @property
    def project_languages(self) -> List[EProjectLanguage]:
        """
        Gets the languages used in the project.
        """
        return self._project_languages


    @property
    def project_all_target_name(self) -> str:
        """
        Gets the name of the project's `all` target.
        """
        return self._project_all_target_name


    @property
    def project_test_target_name(self) -> str:
        """
        Gets the name of the project's `test` target.
        """
        return self._project_test_target_name


    @property
    def target_sets(self) -> Iterable[TargetSet]:
        """
        Gets all target sets in the project.
        """
        return [s for _, s in self._target_sets]


    def add_target_set(self,
        set_name: str,
        all_target_name: str,
        test_target_name: str,
        common_target_name: str) -> TargetSet:
        """
        Adds a target set to the project.
        @param set_name Name of the target set. Must be unique within the
          project scope.
        @param all_target_name Name of the target that builds all targets in the
          set.
        @param test_target_name Name of the target that builds all test targets
          in the set.
        @param common_target_name Name of the set's common interface target.
        """
        target_set = TargetSet(
            set_name,
            all_target_name,
            test_target_name,
            common_target_name
        )

        # Check if the target set already exists
        if set_name in self._target_sets:
            # If the previous target set was declared at the same location,
            #   return it instead of creating a new one or throwing an error.
            prev_set = self._target_sets[set_name]
            if prev_set.origin == target_set.origin:
                return prev_set

            error_str = "Error: Cannot add a target set with the name " + \
                f"'{set_name}' to the project scope " + \
                f"'{self.project_name}'.\n"
            error_str += "Note: A target set with the name " + \
                f"'{set_name}' already exists in the project scope.\n"
            error_str += "    The target set was previously added at " + \
                f"{prev_set.origin.file_path}:" + \
                f"{prev_set.origin.line_number}.\n"
            error_str += "    The new target set is being added at " + \
                f"{target_set.origin.file_path}:" + \
                f"{target_set.origin.line_number}."
            raise RuntimeError(error_str)

        # Add the target set to the project.
        self._target_sets[set_name] = target_set
        return target_set
