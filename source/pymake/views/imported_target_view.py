from __future__ import annotations
from pathlib import Path
from pymake.common.scope import EScope
from pymake.common.target_type import ETargetType
from pymake.model.project_scope import ProjectScope
from pymake.model.pymake_project import PyMakeProject
from pymake.model.target_set import TargetSet
from pymake.model.targets.imported.imported_target import ImportedTarget
from pymake.util.path_statics import PathStatics
from pymake.util.platform_statics import PlatformStatics
from typing import List

class ImportedTargetView:
    """
    Provides an interface for modifying an imported target.
    """
    def __init__(self,
        project: PyMakeProject,
        project_scope: ProjectScope,
        target_set: TargetSet,
        target: ImportedTarget):
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


    @property
    def target_name(self) -> str:
        """
        Gets the name of the target.
        """
        return self._target.target_name


    def add_include_directories(self,
        *include_directories: str) -> None:
        """
        Adds include directories to the target.
        All include directories are added to the `INTERFACE` scope.
        @param include_directories The include directories to add.
        """
        # Convert all include directories to absolute paths.
        paths: List[Path] = []
        for include_directory in include_directories:
            paths.append(PathStatics.resolve_by_caller_path(include_directory))

        interface_set = self._target.properties.include_directories.select_set(
            EScope.INTERFACE
        )
        for path in paths:
            interface_set.add(path)


    def set_location(self,
        dir: str | Path,
        name: str,
        add_prefix_suffix: bool = True) -> None:
        """
        Sets the location of the imported target.
        @param dir The directory that the target is located in. This may be an
          absolute or relative path. If the path is a relative path, it will
          be interpreted relative to the caller's directory.
        @param name Name of the library. This should not include the prefix or
          file extension unless `add_prefix_suffix` is `False`.
        @param add_prefix_suffix Whether to add the platform-specific prefix
          and suffix to the library name.
        """
        # Convert the path to an absolute path
        lib_path = PathStatics.resolve_by_caller_path(dir)

        # Update the library name if necessary
        if add_prefix_suffix:
            name = PlatformStatics.get_static_lib_name(name)

        # This property is only valid on imported interface targets
        if self._target.target_type == ETargetType.INTERFACE:
            self._target.properties.imported_libname = name
        self._target.properties.imported_location = lib_path / name


    def install(self, install_path: str | Path) -> None:
        """
        Installs the target.
        @param install_path The path to install the target to. If this is a
          relative path, it will be interpreted relative to the install prefix.
        """
        self._target.properties.install(install_path)
