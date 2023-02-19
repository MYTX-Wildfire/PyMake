import os
from pathlib import Path
from pymake.core.preset import Preset
from pymake.core.target import Target
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

    def write_preset(self,
        preset: Preset,
        generated_tree_path: Path) -> None:
        """
        Writes the preset out in a human readable form for debugging.
        @param preset Preset to generate a file for.
        @param generated_tree_path Path to the directory where all generated
          files should be placed.
        """
        preset_state = preset.preset_state
        output_file = generated_tree_path.joinpath(
            preset_state.preset_name + ".preset.yaml"
        )
        with open(output_file, mode="w") as f:
            f.write(preset_state.to_yaml())

    def write_target(self,
        target: Target,
        generated_tree_path: Path) -> None:
        """
        Writes the target out in a human readable form for debugging.
        @param target Target to generate a file for.
        @param generated_tree_path Path to the directory where all generated
          files should be placed.
        """
        output_file = generated_tree_path.joinpath(
            target.target_name + ".target.yaml"
        )
        with open(output_file, mode="w") as f:
            f.write(target.to_yaml())
