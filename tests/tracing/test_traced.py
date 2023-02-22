from pymake.tracing.traced import Traced
import pytest
from typing import Any

test_data = [
    1,
    2,
    "foo",
    "bar"
]

@pytest.mark.parametrize("value", test_data)
def test_get_traced_value(value: Any):
    traced = Traced(value)
    assert value == traced.value
