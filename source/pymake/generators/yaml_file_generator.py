from pathlib import Path
from pymake.generators.trace_file_generator import ITraceFileGenerator
from typing import Any
import yaml

class YamlFileGenerator(ITraceFileGenerator):
    """
    Class that generates a YAML file containing tracing information.
    """

    def generate(self, data: Any) -> str:
        """
        Gets the contents of the generated trace file.
        @returns The contents of the generated trace file.
        """
        return yaml.dump(data)


    def write_file(self, data: Any, output_path: str | Path) -> None:
        """
        Writes the generated trace file to the specified path.
        @param output_path Path to write the generated trace file to.
        """
        # Serialize the object as a YAML string and write it to the output path
        with open(output_path, "w") as file:
            file.write(self.generate(data))
