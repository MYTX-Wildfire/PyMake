from pathlib import Path
from pymake.core.build_script_set import BuildScriptSet
from pymake.tracing.null_caller_info_formatter import NullCallerInfoFormatter
from typing import Any

def test_build_script_set_empty_after_construction():
    build_script_set = BuildScriptSet(
        Path("/source"),
        Path("/generated"),
        NullCallerInfoFormatter()
    )
    assert not build_script_set


def test_add_build_script_in_source_tree():
    """
    Verifies that the first time `get_or_add_build_script` is called for a file
      in the source tree, a new build script is added to the set.
    """
    build_script_set = BuildScriptSet(
        Path("/source"),
        Path("/generated"),
        NullCallerInfoFormatter()
    )
    build_script_set.get_or_add_build_script(Path("/source/foo.py"))
    assert build_script_set
    assert len(build_script_set) == 1


def test_add_build_script_outside_source_tree():
    """
    Verifies that the first time `get_or_add_build_script` is called for a file
      outside of the source tree, a new build script is added to the set.
    """
    build_script_set = BuildScriptSet(
        Path("/source"),
        Path("/generated"),
        NullCallerInfoFormatter()
    )
    build_script_set.get_or_add_build_script(Path("/foo/bar.py"))
    assert build_script_set
    assert len(build_script_set) == 1


def test_outside_source_build_script_generated_in_external_dir():
    """
    Verifies that the path to the generated build script for a build script that
      lies outside of the source tree will be in the external directory.
    """
    generated_path = Path("/generated")
    external_path = Path.joinpath(
        generated_path,
        BuildScriptSet.EXTERNAL_GENERATED_DIR
    )
    build_script_set = BuildScriptSet(
        Path("/source"),
        generated_path,
        NullCallerInfoFormatter()
    )
    build_script = build_script_set.get_or_add_build_script(Path("/foo/bar.py"))

    assert str(build_script.target_path).startswith(str(external_path))


def test_get_existing_build_script():
    """
    Verifies that subsequent calls to `get_or_add_build_script` for the same
      file results in the same build script being returned.
    """
    build_script_set = BuildScriptSet(
        Path("/source"),
        Path("/generated"),
        NullCallerInfoFormatter()
    )
    first = build_script_set.get_or_add_build_script()
    second = build_script_set.get_or_add_build_script()

    assert first is second
    assert build_script_set
    assert len(build_script_set) == 1


def test_get_build_script_for_two_different_files():
    """
    Verifies that calls to `get_or_add_build_script` for different files results
      in different build scripts being returned.
    """
    build_script_set = BuildScriptSet(
        Path("/source"),
        Path("/generated"),
        NullCallerInfoFormatter()
    )
    first = build_script_set.get_or_add_build_script(Path("/foo.py"))
    second = build_script_set.get_or_add_build_script(Path("/bar.py"))
    assert first is not second
    assert build_script_set
    assert len(build_script_set) == 2


def test_make_py_generates_cmakelists_txt():
    """
    Verifies that make.py files result in the generation of a CMakeLists.txt file.
    """
    build_script_set = BuildScriptSet(
        Path("/source"),
        Path("/generated"),
        NullCallerInfoFormatter()
    )
    build_script = build_script_set.get_or_add_build_script(Path("/make.py"))
    assert str(build_script.target_path).endswith("CMakeLists.txt")


def test_other_py_files_generate_cmake_files():
    """
    Verifies that non-make.py files result in the generation of a *.cmake file.
    """
    build_script_set = BuildScriptSet(
        Path("/source"),
        Path("/generated"),
        NullCallerInfoFormatter()
    )
    foo = build_script_set.get_or_add_build_script(Path("/foo.py"))
    bar = build_script_set.get_or_add_build_script(Path("/bar.py"))
    assert str(foo.target_path).endswith("foo.cmake")
    assert str(bar.target_path).endswith("bar.cmake")


def test_generate_build_script(tmp_path: Any):
    """
    Verifies that a build script can be generated.
    """
    build_script_set = BuildScriptSet(
        Path("/source"),
        Path(tmp_path),
        NullCallerInfoFormatter()
    )
    build_script = build_script_set.get_or_add_build_script(Path("/foo.py"))
    build_script_set.generate()

    assert Path(build_script.target_path).exists()
