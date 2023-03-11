from pathlib import Path
from pymake.generators.cmake_generator import CMakeGenerator

class BuildScript():
    """
    Stores all data for a CMake build script that must be generated.
    """
    def __init__(self,
        target_path: Path,
        generator: CMakeGenerator):
        """
        Initializes the build script.
        @param target_path Path that the build script should be generated at.
            Must be an absolute path.
        @param generator Generator to use to add CMake code to the build script.
        """
        assert target_path.is_absolute()
        self._target_path = target_path
        self._generator = generator


    @property
    def target_path(self) -> Path:
        """
        Gets the path that the build script should be generated at.
        @invariant This will always be an absolute path.
        """
        return self._target_path


    @property
    def generator(self) -> CMakeGenerator:
        """
        Gets the generator that used to add CMake code to the build script.
        """
        return self._generator


    def write_file(self) -> None:
        """
        Writes the build script to disk.
        """
        self._generator.write_file(self._target_path)
