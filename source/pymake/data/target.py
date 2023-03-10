from __future__ import annotations
from abc import ABC, abstractmethod
from pathlib import Path
from pymake.common.scope import EScope
from pymake.common.target_type import ETargetType
from pymake.common.test_flags import ETestFlags
from pymake.core.build_script import BuildScript
from pymake.tracing.traced import ITraced
from typing import Optional

class ITarget(ABC, ITraced):
    """
    Represents a CMake target within a PyMake project.
    """
    def __init__(self,
        target_name: str,
        target_type: ETargetType,
        sanitizer_flags: int,
        test_flags: int):
        """
        Initializes the target.
        @param target_name The name of the target.
        @param target_type The type of the target.
        @param sanitizer_flags The sanitizers enabled for the target.
        @param test_flags Identifies whether the target is a test target and
          what kind of target the test target is.
        """
        self._target_name = target_name
        self._target_type = target_type
        self._sanitizer_flags = sanitizer_flags
        self._test_flags = test_flags


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


    @property
    def sanitizer_flags(self) -> int:
        """
        Gets the sanitizers enabled for the target.
        """
        return self._sanitizer_flags


    @property
    def test_flags(self) -> int:
        """
        Gets the test flags for the target.
        """
        return self._test_flags


    @property
    def is_test_target(self) -> bool:
        """
        Gets whether the target is a test target.
        """
        return self._test_flags != ETestFlags.NONE


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
        target: ITarget) -> None:
        """
        Links the target to another target.
        @param scope The scope of the link.
        @param target The target to link to.
        """
        raise NotImplementedError()


    def generate_target(self,
        build_script: BuildScript) -> None:
        """
        Generates the CMake code for the target.
        @param build_script Build script to write the target to.
        """
        raise NotImplementedError()


    @abstractmethod
    def _generate_declaration(self,
        build_script: BuildScript) -> None:
        """
        Generates the CMake code for the declaration of the target.
        @param build_script Build script to write the target to.
        """
        raise NotImplementedError()
