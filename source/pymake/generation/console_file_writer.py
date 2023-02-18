from pathlib import Path
from pymake.generation.file_writer import IFileWriter
from pymake.generation.build_script import BuildScript

class ConsoleFileWriter(IFileWriter):
    """
    File writer that writes to stdout instead of files on disk.
    """
    def write_script(self,
        build_script: BuildScript,
        source_tree_path: Path) -> None:
        """
        Method invoked to write a script via the writer.
        @param build_script Build script to write out.
        @param source_tree_path Absolute path to the root of the source tree.
        """
        print(f"File: {build_script.target_path}")
        print("========================================")
        print(build_script.generate_file_contents(source_tree_path))
        print("========================================")

