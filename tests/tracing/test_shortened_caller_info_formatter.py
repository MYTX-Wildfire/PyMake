from dummy_traced import DummyTraced
from pathlib import Path
from pymake.tracing.caller_info import CallerInfo
from pymake.tracing.shortened_caller_info_formatter import ShortenedCallerInfoFormatter
from pymake.tracing.traced import Traced

def test_shortened_caller_info_formatter_on_caller_info_full_path():
    """
    Verifies the formatter's output when `format()` is called with a `CallerInfo`
      instance where the stored path is not related to the formatter's base
      path.
    """
    formatter = ShortenedCallerInfoFormatter("/foo/bar")
    line_num = 123
    caller_info = CallerInfo(__file__, line_num)

    output = formatter.format(caller_info)
    assert __file__ in output
    assert str(line_num) in output


def test_shortened_caller_info_formatter_on_caller_info_shortened_path():
    """
    Verifies the formatter's output when `format()` is called with a `CallerInfo`
      instance where the stored path is related to the formatter's base path.
    """
    base_dir = Path(__file__).parent
    curr_file_name = Path(__file__).name

    formatter = ShortenedCallerInfoFormatter(base_dir)
    line_num = 123
    caller_info = CallerInfo(__file__, line_num)

    output = formatter.format(caller_info)
    # The full path should not be in the output
    assert __file__ not in output
    assert curr_file_name in output
    assert str(line_num) in output


def test_shortened_caller_info_formatter_on_traced_full_path():
    """
    Verifies the formatter's output when `format()` is called with a `Traced`
      instance where the stored path is not related to the formatter's base path.
    """
    formatter = ShortenedCallerInfoFormatter("/foo/bar")
    line_num = 123
    caller_info = CallerInfo(__file__, line_num)
    traced = Traced("foo", caller_info)

    output = formatter.format(traced)
    assert __file__ in output
    assert str(line_num) in output


def test_shortened_caller_info_formatter_on_traced_shortened_path():
    """
    Verifies the formatter's output when `format()` is called with a `Traced`
      instance where the stored path is related to the formatter's base path.
    """
    base_dir = Path(__file__).parent
    curr_file_name = Path(__file__).name

    formatter = ShortenedCallerInfoFormatter(base_dir)
    line_num = 123
    caller_info = CallerInfo(__file__, line_num)
    traced = Traced("foo", caller_info)

    output = formatter.format(traced)
    # The full path should not be in the output
    assert __file__ not in output
    assert curr_file_name in output
    assert str(line_num) in output


def test_shortened_caller_info_formatter_on_traced_class_full_path():
    """
    Verifies the formatter's output when `format()` is called with an `ITraced`
      instance where the stored path is not related to the formatter's base path.
    """
    formatter = ShortenedCallerInfoFormatter("/foo/bar")
    line_num = 123
    caller_info = CallerInfo(__file__, line_num)
    traced = DummyTraced(caller_info)

    output = formatter.format(traced)
    assert __file__ in output
    assert str(line_num) in output


def test_shortened_caller_info_formatter_on_traced_class_shortened_path():
    """
    Verifies the formatter's output when `format()` is called with an `ITraced`
      instance where the stored path is related to the formatter's base path.
    """
    base_dir = Path(__file__).parent
    curr_file_name = Path(__file__).name

    formatter = ShortenedCallerInfoFormatter(base_dir)
    line_num = 123
    caller_info = CallerInfo(__file__, line_num)
    traced = DummyTraced(caller_info)

    output = formatter.format(traced)
    # The full path should not be in the output
    assert __file__ not in output
    assert curr_file_name in output
    assert str(line_num) in output
