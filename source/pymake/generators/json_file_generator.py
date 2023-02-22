import json
from pathlib import Path
from pymake.generators.trace_file_generator import ITraceFileGenerator
from typing import Any

class JsonFileGenerator(ITraceFileGenerator):
    """
    Class that generates a JSON file containing tracing information.
    """

    def generate(self, data: Any) -> str:
        """
        Gets the contents of the generated trace file.
        @returns The contents of the generated trace file.
        """
        return json.dumps(data, indent=4)


    def write_file(self, data: Any, output_path: str | Path) -> None:
        """
        Writes the generated trace file to the specified path.
        @param output_path Path to write the generated trace file to.
        """
        # Serialize the object as a JSON string and write it to the output path
        with open(output_path, "w") as file:
            file.write(self.generate(data))
