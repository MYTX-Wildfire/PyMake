from abc import ABC, abstractmethod
from pathlib import Path
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
