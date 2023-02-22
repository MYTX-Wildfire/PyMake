import pytest
from pathlib import Path
from pymake.tracing.caller_info import CallerInfo

def test_closest_external_frame():
    """
    Verifies that the `closest_external_frame()` method returns a caller info
      capturing this method.
    """
    caller_info = CallerInfo.closest_external_frame()
    assert str(caller_info.file_path) == __file__
    assert caller_info.line_number == 10


def test_from_stack_frame():
    """
    Verifies that this method's stack frame can be captured using
      `CallerInfo.from_stack_frame()`
    """
    caller_info = CallerInfo.from_stack_frame(0)
    assert str(caller_info.file_path) == __file__
    assert caller_info.line_number == 20


def test_hash_and_equality():
    caller_info1 = CallerInfo(Path("/foo.py"), 1)
    caller_info2 = CallerInfo(Path("/foo.py"), 1)
    assert caller_info1 == caller_info2
    assert hash(caller_info1) == hash(caller_info2)

    caller_info3 = CallerInfo(Path("/bar.py"), 1)
    assert caller_info1 != caller_info3
    assert hash(caller_info1) != hash(caller_info3)

    caller_info4 = CallerInfo(Path("/foo.py"), 2)
    assert caller_info1 != caller_info4
    assert hash(caller_info1) != hash(caller_info4)

    assert caller_info1 != 1
    assert caller_info1 != "foo"
    assert caller_info1 != None


def test_ctor_throws_if_path_not_absolute():
    with pytest.raises(ValueError):
        CallerInfo("foo.py", 1)
