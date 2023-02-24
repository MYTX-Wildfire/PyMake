from pymake.generators.yaml_file_generator import YamlFileGenerator
from typing import Any

def test_serialize_single_key_value_pair():
    # Create the generator
    generator = YamlFileGenerator()

    # Serialize the value
    result = generator.generate({
        "key": "value"
    })

    # Verify the result
    assert result == "key: value\n"


def test_serialize_single_array():
    # Create the generator
    generator = YamlFileGenerator()

    # Serialize the value
    result = generator.generate([
        "value"
    ])

    # Verify the result
    assert result == "- value\n"


def test_write_to_file(tmp_path: Any):
    # Create the generator
    generator = YamlFileGenerator()

    # Serialize the value
    output_path = tmp_path / "output.yaml"
    generator.write_file({
        "key": "value"
    }, output_path)

    # Verify the result
    with open(output_path, "r") as file:
        result = file.read()
    assert result == "key: value\n"
