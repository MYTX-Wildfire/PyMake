from pymake.tracing.caller_info import CallerInfo
from pymake.tracing.full_caller_info_formatter import FullCallerInfoFormatter
from pymake.tracing.traced import ITraced, Traced

class DummyTraced(ITraced):
    """
    Helper class that implements `ITraced`.
    """
    def __init__(self, origin: CallerInfo):
        """
        Initializes the instance.
        @param origin Value to store as the origin of the object.
        """
        self._origin = origin

    @property
    def origin(self) -> CallerInfo:
        """
        Gets the location that constructed the object.
        """
        return self._origin

def test_full_caller_info_formatter_on_caller_info():
    """
    Verifies the formatter's output when `format()` is called with a `CallerInfo`
      instance.
    """
    formatter = FullCallerInfoFormatter()
    line_num = 123
    caller_info = CallerInfo(__file__, line_num)

    output = formatter.format(caller_info)
    assert __file__ in output
    assert str(line_num) in output

def test_full_caller_info_formatter_on_traced():
    """
    Verifies the formatter's output when `format()` is called with a `Traced`
      instance.
    """
    formatter = FullCallerInfoFormatter()
    line_num = 123
    caller_info = CallerInfo(__file__, line_num)
    traced = Traced("foo", caller_info)

    output = formatter.format(traced)
    assert __file__ in output
    assert str(line_num) in output

def test_full_caller_info_formatter_on_traced_class():
    """
    Verifies the formatter's output when `format()` is called with an `ITraced`
      instance.
    """
    formatter = FullCallerInfoFormatter()
    line_num = 123
    caller_info = CallerInfo(__file__, line_num)
    traced = DummyTraced(caller_info)

    output = formatter.format(traced)
    assert __file__ in output
    assert str(line_num) in output
