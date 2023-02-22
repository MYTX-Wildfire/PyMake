from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

class ITraceFileGenerator(ABC):
    """
    Base class for types that generate trace files.
    """

    @abstractmethod
    def generate(self, data: Any) -> str:
        """
        Gets the contents of the generated trace file.
        @returns The contents of the generated trace file.
        """
        raise NotImplementedError()


    @abstractmethod
    def write_file(self, data: Any, output_path: str | Path) -> None:
        """
        Writes the generated trace file to the specified path.
        @param output_path Path to write the generated trace file to.
        """
        raise NotImplementedError()
