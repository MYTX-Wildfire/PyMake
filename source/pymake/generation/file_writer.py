from abc import ABC, abstractmethod
from pathlib import Path
from pymake.core.preset import Preset
from pymake.core.target import Target
from pymake.generation.build_script import BuildScript

class IFileWriter(ABC):
    """
    Base interface for classes that process generated build scripts.
    """
    @abstractmethod
    def write_script(self,
        build_script: BuildScript,
        source_tree_path: Path) -> None:
        """
        Method invoked to write a script via the writer.
        @param build_script Build script to write out.
        @param source_tree_path Absolute path to the root of the source tree.
        """
        raise NotImplementedError()

    @abstractmethod
    def write_preset(self,
        preset: Preset,
        generated_tree_path: Path) -> None:
        """
        Writes the preset out in a human readable form for debugging.
        @param preset Preset to generate a file for.
        @param generated_tree_path Path to the directory where all generated
          files should be placed.
        """
        raise NotImplementedError()

    @abstractmethod
    def write_target(self,
        target: Target,
        generated_tree_path: Path) -> None:
        """
        Writes the target out in a human readable form for debugging.
        @param target Target to generate a file for.
        @param generated_tree_path Path to the directory where all generated
          files should be placed.
        """
        raise NotImplementedError()
