from __future__ import annotations
from pathlib import Path
from pymake.common.scope import EScope
from pymake.common.target_type import ETargetType
from pymake.model.targets.target import Target
from typing import Optional

class BuildTarget(Target):
    """
    Represents a target that must be built by CMake.
    """
    def __init__(self,
        target_name: str,
        target_type: ETargetType,
        test_flags: int,
        sanitizer_flags: int):
        """
        Initializes the target.
        @param target_name The name of the target.
        @param target_type The type of the target.
        @param test_flags Identifies whether the target is a test target and
          what kind of target the test target is.
        @param sanitizer_flags The sanitizers enabled for the target.
        """
        super().__init__(
            target_name,
            test_flags,
            sanitizer_flags
        )
        self._target_type = target_type


    @property
    def target_type(self) -> ETargetType:
        """
        Gets the type of the target.
        """
        return self._target_type


    def add_include_directory(self,
        scope: EScope,
        include_directory: Path) -> None:
        """
        Adds an include directory to the target.
        @param scope The scope of the include directory.
        @param include_directory The include directory to add. Must be an
          absolute path.
        """
        raise NotImplementedError()


    def add_compile_definition(self,
        scope: EScope,
        compile_definition: str,
        value: Optional[str]) -> None:
        """
        Adds a compile definition to the target.
        @param scope The scope of the compile definition.
        @param compile_definition The compile definition to add.
        @param value The value of the compile definition. If None, the compile
          definition will be added without a value.
        """
        raise NotImplementedError()


    def add_compile_option(self,
        scope: EScope,
        compile_option: str) -> None:
        """
        Adds a compile option to the target.
        @param scope The scope of the compile option.
        @param compile_option The compile option to add.
        """
        raise NotImplementedError()


    def add_source_file(self,
        scope: EScope,
        source_file: Path) -> None:
        """
        Adds a source file to the target.
        @param scope The scope of the source file.
        @param source_file The source file to add. Must be an absolute path.
        """
        raise NotImplementedError()


    def link_to(self,
        scope: EScope,
        target: Target) -> None:
        """
        Links the target to another target.
        @param scope The scope of the link.
        @param target The target to link to.
        """
        raise NotImplementedError()
