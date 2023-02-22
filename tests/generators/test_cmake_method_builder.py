from pymake.generators.cmake_generator import CMakeGenerator
from pymake.tracing.null_caller_info_formatter import NullCallerInfoFormatter
from tests.tracing.mock_caller_info_formatter import MockCallerInfoFormatter

def test_generate_empty_method():
    """
    Tests generating an empty CMake method.
    """
    generator = CMakeGenerator(NullCallerInfoFormatter())
    with generator.open_method_block("foo") as _:
        pass
    assert generator.generate() == "foo()\n"


def test_tracing_information():
    generator = CMakeGenerator(MockCallerInfoFormatter("foobar"))
    with generator.open_method_block("method") as _:
        pass
    assert generator.generate().startswith("# foobar\n")


def test_generate_method_with_single_argument():
    generator = CMakeGenerator(NullCallerInfoFormatter())
    with generator.open_method_block("foo") as method:
        method.add_arguments("bar")

    cmake_code = generator.generate()
    tokens = cmake_code.splitlines()
    expected_tokens = [
        "foo(",
        "\tbar",
        ")",
    ]
    assert expected_tokens == tokens


def test_generate_method_with_arguments():
    generator = CMakeGenerator(NullCallerInfoFormatter())
    with generator.open_method_block("foo") as method:
        method.add_arguments(["bar", "baz"])

    cmake_code = generator.generate()
    tokens = cmake_code.splitlines()
    expected_tokens = [
        "foo(",
        "\tbar",
        "\tbaz",
        ")",
    ]
    assert expected_tokens == tokens


def test_generate_method_with_single_keyword_argument():
    generator = CMakeGenerator(NullCallerInfoFormatter())
    with generator.open_method_block("foo") as method:
        method.add_keyword_arguments("KEYWORD", "bar")

    cmake_code = generator.generate()
    tokens = cmake_code.splitlines()
    expected_tokens = [
        "foo(",
        "\tKEYWORD",
        "\t\tbar",
        ")",
    ]
    assert expected_tokens == tokens


def test_generate_method_with_keyword_arguments():
    generator = CMakeGenerator(NullCallerInfoFormatter())
    with generator.open_method_block("foo") as method:
        method.add_keyword_arguments("KEYWORD", ["bar", "baz"])

    cmake_code = generator.generate()
    tokens = cmake_code.splitlines()
    expected_tokens = [
        "foo(",
        "\tKEYWORD",
        "\t\tbar",
        "\t\tbaz",
        ")",
    ]
    assert expected_tokens == tokens
