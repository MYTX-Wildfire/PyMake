from pathlib import Path
import os

class PathStatics:
    """
    Defines various static helper functions for dealing with paths.
    """
    @staticmethod
    def validate_file(
        file_path: str | Path,
        base_path: Path,
        resolve_strings_using_path: bool) -> Path:
        """
        Validates that the given path exists and is a file.
        @param file_path The path to validate. This may be an absolute or
          relative path. If the path is relative, it will be resolved relative
          to the base path. If this is a string, it will be interpreted as a
          path if `resolve_strings_using_path` is True, otherwise it will be
          interpreted as a file name that must be resolved using the system
          PATH.
        @throws ValueError Thrown if the path does not exist or is not to a file.
        @throws FileNotFoundError Thrown if the path is a string and cannot be
          resolved using the system PATH.
        @returns The resolved absolute path.
        """
        # If resolving via the PATH was not requested, treat strings as paths.
        if isinstance(file_path, str) and not resolve_strings_using_path:
            file_path = Path(file_path)
        elif isinstance(file_path, str):
            # Resolve the path using the system PATH.
            for path in os.environ["PATH"].split(os.pathsep):
                candidate_path = Path(path).joinpath(file_path)
                if os.path.isfile(candidate_path):
                    return candidate_path
            raise FileNotFoundError(
                f"Could not find a file with name '{file_path}' on the PATH."
            )

        # Resolve the path.
        if not file_path.is_absolute():
            file_path = base_path / file_path
        file_path = file_path.resolve()

        if not file_path.exists():
            raise ValueError(f'Path "{file_path}" does not exist.')

        if not file_path.is_file():
            raise ValueError(f'Path "{file_path}" is not a file.')

        return file_path
