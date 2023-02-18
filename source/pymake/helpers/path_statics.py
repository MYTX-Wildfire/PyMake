from pathlib import Path

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
