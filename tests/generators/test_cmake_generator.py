import os
from pymake.generators.cmake_generator import CMakeGenerator
from pymake.tracing.null_caller_info_formatter import NullCallerInfoFormatter
from typing import Any

def test_generate_method():
    generator = CMakeGenerator(NullCallerInfoFormatter())
    with generator.open_method_block("foo") as _:
        pass

    cmake_code = generator.generate()
    assert cmake_code == "foo()\n\n"


def test_generate_file(tmp_path: Any):
    generator = CMakeGenerator(NullCallerInfoFormatter())
    with generator.open_method_block("foo") as _:
        pass

    output_path = tmp_path / "test.cmake"
    generator.write_file(output_path)
    with open(output_path, "r") as f:
        assert f.read() == "foo()\n\n"
    os.remove(output_path)
