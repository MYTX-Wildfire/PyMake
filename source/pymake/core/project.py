from pymake.common.project_language import EProjectLanguage
from pymake.core.build_script_set import BuildScriptSet
from pymake.core.executable_target import ExecutableTarget
from pymake.core.shared_library_target import SharedLibraryTarget
from pymake.core.static_library_target import StaticLibraryTarget
from pymake.core.target import ITarget
from pymake.tracing.traced import ITraced
from typing import Callable, Dict, Iterable, Optional

class Project(ITraced):
    """
    Represents a single project scope in a PyMake project.
    """
    def __init__(self,
        build_scripts: BuildScriptSet,
        project_name: str,
        project_languages: EProjectLanguage | Iterable[EProjectLanguage]):
        """
        Initializes the project.
        @param build_scripts Set of build scripts that the project will generate.
        @param project_name Name of the project.
        @param project_languages Languages used in the project.
        """
        super().__init__()
        self._build_scripts = build_scripts
        self._project_name = project_name
        self._project_languages = list(project_languages) if isinstance(
            project_languages, Iterable) else [project_languages]

        # Callback that will be invoked when a target is added
        # The callback will be passed the target that was just added as its only
        #   parameter. If a target was already added with the given name, the
        #   previously added target must be returned.
        self._on_target_added: Callable[[ITarget], Optional[ITarget]] = \
            lambda target: None

        # Collections of untraced values
        # These values are stored as-is instead of in `Traced` objects since
        #   each instance manages its own tracing information
        self._targets: Dict[str, ITarget] = {}

        # Generate the CMake code
        generator = self._build_scripts.get_or_add_build_script().generator
        with generator.open_method_block("project") as b:
            b.add_arguments(self._project_name)
            b.add_keyword_arguments(
                "LANGUAGES",
                [l.value for l in self._project_languages]
            )


    @property
    def project_name(self) -> str:
        """
        Gets the name of the project.
        """
        return self._project_name


    @property
    def project_languages(self) -> Iterable[EProjectLanguage]:
        """
        Gets the languages used in the project.
        """
        return self._project_languages


    def add_executable(self,
        target_name: str) -> ExecutableTarget:
        """
        Adds an executable target to the project.
        @param target_name Name of the target.
        @throws ValueError Thrown if a target with the given name already exists.
        @returns The target instance.
        """
        target = ExecutableTarget(
            self._build_scripts,
            target_name
        )

        # Check if a target with the given name already exists
        prev_target = self._check_is_target_redefined(target)
        if prev_target:
            assert isinstance(prev_target, ExecutableTarget)
            return prev_target

        # Add the target to the project
        target.generate_declaration()
        self._targets[target_name] = target
        return target


    def add_static_library(self,
        target_name: str) -> StaticLibraryTarget:
        """
        Adds a static library target to the project.
        @param target_name Name of the target.
        @throws ValueError Thrown if a target with the given name already exists.
        @returns The target instance.
        """
        target = StaticLibraryTarget(
            self._build_scripts,
            target_name
        )

        # Check if a target with the given name already exists
        prev_target = self._check_is_target_redefined(target)
        if prev_target:
            assert isinstance(prev_target, StaticLibraryTarget)
            return prev_target

        # Add the target to the project
        target.generate_declaration()
        self._targets[target_name] = target
        return target


    def add_shared_library(self,
        target_name: str) -> SharedLibraryTarget:
        """
        Adds a shared library target to the project.
        @param target_name Name of the target.
        @throws ValueError Thrown if a target with the given name already exists.
        @returns The target instance.
        """
        target = SharedLibraryTarget(
            self._build_scripts,
            target_name
        )

        # Check if a target with the given name already exists
        prev_target = self._check_is_target_redefined(target)
        if prev_target:
            assert isinstance(prev_target, SharedLibraryTarget)
            return prev_target

        # Add the target to the project
        target.generate_declaration()
        self._targets[target_name] = target
        return target


    def _check_is_target_redefined(self,
        target: ITarget) -> Optional[ITarget]:
        """
        Checks if the given target is being redefined.
        @param target Target to check.
        @throws ValueError Thrown if the target is being redefined at a
          different location.
        @returns The previously added target if it was defined at the same
          location as the target being added, `None` otherwise. If a target
          is returned, the returned target is guaranteed to be the same type as
          `target`.
        """
        # Check if a target with the given name already exists
        prev_target = self._on_target_added(target)
        if prev_target:
            # If the previously added target is defined at the same location as
            #   the target being added, return the previously added target
            # This is necessary to allow build scripts to import targets from
            #   other build scripts while also allowing build scripts to contain
            #   code in the top-level scope.
            if prev_target.origin.file_path == target.origin.file_path and \
                prev_target.origin.line_number == target.origin.line_number:
                return prev_target

            error_str = "Error: A target with the name " + \
                f"'{target.target_name}' already exists.\n"
            error_str += "Note: The target was previously added at " + \
                f"{prev_target.origin.file_path}:" + \
                f"{prev_target.origin.line_number}\n"
            error_str += "Note: Target is being redefined at " + \
                f"{target.origin.file_path}:" + \
                f"{target.origin.line_number}"
            raise ValueError(error_str)

        return None


    def _set_on_target_added(self,
        callback: Callable[[ITarget], None]) -> None:
        """
        Sets the callback that will be invoked when a target is added.
        @param callback Callback to invoke when a target is added to the project.
        """
        self._on_target_added = callback


    # Allow external objects to bind to the `on_target_added` event
    on_target_added = property(fset=_set_on_target_added)
