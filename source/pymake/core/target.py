from __future__ import annotations
from abc import ABC, abstractmethod
from pathlib import Path
from pymake.common.scope import EScope
from pymake.common.target_type import ETargetType
from pymake.core.scoped_sets import ScopedSets
from pymake.tracing.caller_info import CallerInfo
from pymake.tracing.traced import ITraced, Traced
from typing import Iterable, Optional

class ITarget(ABC, ITraced):
    """
    Represents a single CMake target.
    """
    def __init__(self,
        target_name: str,
        target_type: ETargetType):
        """
        Initializes the target.
        @param target_name Name of the target.
        @param target_type Type of the target.
        """
        super().__init__()
        self._target_name = target_name
        self._target_type = target_type
        self._is_full_target = False

        # Properties for the target
        # Note that each of these collections does *not* include values that
        #   were added to targets that this target links to. To get a target
        #   instance with all values, use the `get_full_target()` method.
        self._sources: ScopedSets[Path] = ScopedSets()

        # Whether the target will be installed
        # If `_is_installed` is `True` but `_install_path` is `None`, the path
        #   that the target will be installed to will be CMake's default path
        #   for the target type.
        self._is_installed = False
        self._install_path: Optional[Traced[str]] = None


    @property
    def is_installed(self) -> bool:
        """
        Gets whether the target will be installed.
        """
        return self._is_installed


    @property
    def install_path(self) -> Optional[Traced[str]]:
        """
        Gets the path that the target will be installed to.
        """
        return self._install_path


    @property
    def is_full_target(self) -> bool:
        """
        Gets whether the target includes all values from targets that it links to.
        """
        return self._is_full_target


    @property
    def target_name(self) -> str:
        """
        Gets the name of the target.
        """
        return self._target_name


    @property
    def target_type(self) -> ETargetType:
        """
        Gets the type of the target.
        """
        return self._target_type


    def add_sources(self,
        sources: str | Iterable[str],
        scope: EScope = EScope.PRIVATE) -> None:
        """
        Adds source files to the target.
        @param sources Source files to add to the target. If any path is a
          relative path, it will be interpreted relative to the caller's
          directory.
        @param scope Scope of the source files.
        """
        if isinstance(sources, str):
            sources = [sources]

        # Get the path of the caller
        # Any relative paths will be interpreted relative to this path.
        caller_info = CallerInfo.closest_external_frame()
        caller_path = Path(caller_info.file_path).parent

        for source in sources:
            # Convert all paths to absolute paths if they aren't already
            path = Path(source)
            if not path.is_absolute():
                path = caller_path / path

            self._sources.select_set(scope).add(path)


    @abstractmethod
    def get_full_target(self) -> ITarget:
        """
        Gets a target instance that includes all values for the target.
        Target instances normally do not include values from targets that
          they link to. The target instance returned by this method contains
          all values for the target, including values from linked-to targets.
        @returns A target instance that includes all values from targets that
          this target links to.
        """
        raise NotImplementedError()


    def install(self,
        install_path: Optional[str] = None) -> None:
        """
        Installs the target.
        @param install_path Path to install the target to. If this is `None`,
          the path that the target will be installed to will be CMake's default
          path for the target type.
        """
        self._is_installed = True
        if install_path:
            self._install_path = Traced(install_path)
