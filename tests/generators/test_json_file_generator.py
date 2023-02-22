from pymake.generators.json_file_generator import JsonFileGenerator
from typing import Any

def test_serialize_single_key_value_pair():
    # Create the generator
    generator = JsonFileGenerator()

    # Serialize the value
    result = generator.generate({
        "key": "value"
    })

    # Verify the result
    tokens = [l.strip() for l in result.split("\n")]
    expected_tokens = [
        "{",
        "\"key\": \"value\"",
        "}",
    ]
    assert tokens == expected_tokens


def test_serialize_single_array():
    # Create the generator
    generator = JsonFileGenerator()

    # Serialize the value
    result = generator.generate([
        "value"
    ])

    # Verify the result
    tokens = [l.strip() for l in result.split("\n")]
    expected_tokens = [
        "[",
        "\"value\"",
        "]",
    ]
    assert tokens == expected_tokens


def test_write_to_file(tmp_path: Any):
    # Create the generator
    generator = JsonFileGenerator()

    # Serialize the value
    output_path = tmp_path / "output.json"
    generator.write_file({
        "key": "value"
    }, output_path)

    # Verify the result
    with open(output_path, "r") as file:
        result = file.read()
    tokens = [l.strip() for l in result.split("\n")]
    expected_tokens = [
        "{",
        "\"key\": \"value\"",
        "}",
    ]
    assert tokens == expected_tokens
