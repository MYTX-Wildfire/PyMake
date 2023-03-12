from pathlib import Path
from pymake.common.scope import EScope
from pymake.model.project_scope import ProjectScope
from pymake.model.pymake_project import PyMakeProject
from pymake.model.target_set import TargetSet
from pymake.model.targets.build.executable_target import ExecutableTarget
from pymake.util.path_statics import PathStatics
from typing import List

class ExecutableTargetView:
    """
    Provides an interface for modifying an executable target.
    """
    def __init__(self,
        project: PyMakeProject,
        project_scope: ProjectScope,
        target_set: TargetSet,
        target: ExecutableTarget):
        """
        Initializes the target view.
        @param project The project that the target is part of.
        @param project_scope The project scope that the target is part of.
        @param target_set The target set that the target is part of.
        @param target The target to provide a view for.
        """
        self._project = project
        self._project_scope = project_scope
        self._target_set = target_set
        self._target = target


    def add_sources(self,
        scope: EScope,
        *sources: str) -> None:
        """
        Adds source files to the target.
        @param sources The source files to add.
        """
        # Convert all sources to absolute paths.
        paths: List[Path] = []
        for source in sources:
            paths.append(PathStatics.resolve_by_caller_path(source))

        self._target.properties.sources.select_set(scope).add(*paths)
