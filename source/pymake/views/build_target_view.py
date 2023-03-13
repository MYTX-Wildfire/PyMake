from __future__ import annotations
from pathlib import Path
from pymake.common.scope import EScope
from pymake.model.project_scope import ProjectScope
from pymake.model.pymake_project import PyMakeProject
from pymake.model.target_set import TargetSet
from pymake.model.targets.build.build_target import BuildTarget
from pymake.util.path_statics import PathStatics
from typing import List

class BuildTargetView:
    """
    Provides an interface for modifying a build target.
    """
    def __init__(self,
        project: PyMakeProject,
        project_scope: ProjectScope,
        target_set: TargetSet,
        target: BuildTarget):
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

        for path in paths:
            self._target.properties.sources.select_set(scope).add(path)


    def add_include_directories(self,
        scope: EScope,
        *include_directories: str) -> None:
        """
        Adds include directories to the target.
        @param include_directories The include directories to add.
        """
        # Convert all include directories to absolute paths.
        paths: List[Path] = []
        for include_directory in include_directories:
            paths.append(PathStatics.resolve_by_caller_path(include_directory))

        for path in paths:
            self._target.properties.include_directories.select_set(scope).add(
                path
            )


    def link_to(self,
        scope: EScope,
        *targets: BuildTargetView) -> None:
        """
        Links the target to other targets.
        @param targets The targets to link to.
        """
        for target in targets:
            self._target.properties.link_libraries.select_set(scope).add(
                target._target.target_name
            )


    def install(self, install_path: str | Path | None = None) -> None:
        """
        Installs the target.
        @param install_path The path to install the target to. If this is a
          relative path, it will be interpreted relative to the install prefix.
          If this is `None`, the target will be installed to CMake's default
          install path for the target type.
        """
        self._target.properties.install(install_path)
