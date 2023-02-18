from pathlib import Path

def to_abs_path(target_path: Path, base_dir: Path) -> Path:
    """
    Converts the target path to an absolute path.
    @param target_path Path to convert. May be a relative or absolute path.
    @param base_dir Path to a directory. Must be an absolute path.
    @returns If the target path is an absolute path, returns the target path
      without modifying it. If the target path is a relative path, interprets
      the target path as a path relative to `base_dir` and returns the resulting
      absolute path.
    """
    assert base_dir.is_absolute()
    if target_path.is_absolute():
        return target_path
    return base_dir.joinpath(target_path).resolve()


def shorten_path(target_path: Path, root_path: Path) -> Path:
    """
    Conditionally shortens the target path if it's below the root path.
    @param target_path Absolute path to conditionally shorten.
    @param root_path Absolute path to the root directory that paths should
        be made relative to. Should not contain any symlinks.
    @returns The target path as a path relative to the root path if the
        target path is under the root path. If the target path is outside
        the root path, returns the target path as-is.
    """
    try:
        path = target_path.resolve()
        return path.relative_to(root_path)
    except ValueError:
        # The build script is not located under the root path. Use the full
        #   path to the file instead.
        return target_path
