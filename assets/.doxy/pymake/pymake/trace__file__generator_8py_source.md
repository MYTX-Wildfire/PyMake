
# File trace\_file\_generator.py

[**File List**](files.md) **>** [**generators**](dir_37593b55cf35ebc86f5d534ab79306ef.md) **>** [**trace\_file\_generator.py**](trace__file__generator_8py.md)

[Go to the documentation of this file.](trace__file__generator_8py.md) 

```Python

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

```