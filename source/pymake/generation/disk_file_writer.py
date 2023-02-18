import os
from pathlib import Path
from pymake.generation.file_writer import IFileWriter
from pymake.generation.build_script import BuildScript

class DiskFileWriter(IFileWriter):
    """
    File writer that writes to files on disk.
    """
    def write_script(self,
        build_script: BuildScript,
        source_tree_path: Path) -> None:
        """
        Method invoked to write a script via the writer.
        @param build_script Build script to write out.
        @param source_tree_path Absolute path to the root of the source tree.
        """
        # Path to the file to generate
        script_path = build_script.target_path

        # Make sure the directories leading to the target path exist
        output_dir = script_path.parent
        os.makedirs(output_dir, exist_ok=True)

        # Generate the file
        with open(script_path, mode="w") as f:
            f.write(build_script.generate_file_contents(source_tree_path))
