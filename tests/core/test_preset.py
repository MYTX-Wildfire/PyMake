from pathlib import Path
from pymake.common.cmake_build_type import ECMakeBuildType
from pymake.common.cmake_generator import ECMakeGenerator
from pymake.core.preset import Preset
from pymake.generators.yaml_file_generator import YamlFileGenerator
from typing import Any

def test_preset_name_matches_ctor_arg():
    preset_name = "foo"
    preset = Preset(preset_name)
    assert preset.preset_name == preset_name


def test_preset_defaults():
    preset = Preset("foo")
    assert not preset.description
    assert not preset.hidden
    assert not preset.generator
    assert not preset.binary_dir
    assert not preset.install_dir
    assert not preset.cache_variables
    assert not preset.env_variables
    assert not preset.cmake_build_type


def test_set_preset_description_via_ctor():
    preset_description = "foo"
    preset = Preset("foo", preset_description)
    assert preset.description == preset_description


def test_set_preset_description_via_property():
    preset_description = "foo"
    preset = Preset("foo")
    preset.description = preset_description
    assert preset.description == preset_description


def test_set_preset_hidden_via_ctor():
    preset = Preset("foo", is_hidden=True)
    assert preset.hidden


def test_set_preset_hidden_via_property():
    preset = Preset("foo")
    preset.hidden = True
    assert preset.hidden


def test_set_preset_generator_via_ctor():
    preset_generator = "foo"
    preset = Preset("foo", cmake_generator=preset_generator)
    assert preset.generator == preset_generator


def test_set_preset_generator_via_property():
    preset_generator = "foo"
    preset = Preset("foo")
    preset.generator = preset_generator
    assert preset.generator == preset_generator


def test_set_preset_generator_using_enum_via_ctor():
    preset_generator = ECMakeGenerator.Ninja
    preset = Preset("foo", cmake_generator=preset_generator)
    assert preset.generator == preset_generator.value


def test_set_preset_generator_using_enum_via_property():
    preset_generator = ECMakeGenerator.Ninja
    preset = Preset("foo")
    preset.generator = preset_generator
    assert preset.generator == preset_generator.value


def test_set_preset_binary_dir_via_ctor():
    preset_binary_dir = "foo"
    preset = Preset("foo", binary_path=preset_binary_dir)
    assert preset.binary_dir == preset_binary_dir


def test_set_preset_binary_dir_via_property():
    preset_binary_dir = "foo"
    preset = Preset("foo")
    preset.binary_dir = preset_binary_dir
    assert preset.binary_dir == preset_binary_dir


def test_set_preset_install_dir_via_ctor():
    preset_install_dir = "foo"
    preset = Preset("foo", install_path=preset_install_dir)
    assert preset.install_dir == preset_install_dir


def test_set_preset_install_dir_via_property():
    preset_install_dir = "foo"
    preset = Preset("foo")
    preset.install_dir = preset_install_dir
    assert preset.install_dir == preset_install_dir


def test_set_preset_cache_variables_via_ctor():
    preset_cache_variables = {"foo": "bar"}
    preset = Preset("foo", cache_vars=preset_cache_variables)
    assert preset.cache_variables == preset_cache_variables


def test_set_preset_cache_variables_via_method():
    preset_cache_variables = {"foo": "bar"}
    preset = Preset("foo")
    for k, v in preset_cache_variables.items():
        preset.set_cache_variable(k, v)
    assert preset.cache_variables == preset_cache_variables


def test_set_preset_env_variables_via_ctor():
    preset_env_variables = {"foo": "bar"}
    preset = Preset("foo", env_vars=preset_env_variables)
    assert preset.env_variables == preset_env_variables


def test_set_preset_env_variables_via_method():
    preset_env_variables = {"foo": "bar"}
    preset = Preset("foo")
    for k, v in preset_env_variables.items():
        preset.set_env_variable(k, v)
    assert preset.env_variables == preset_env_variables


def test_set_preset_single_base_preset_via_ctor():
    base_preset = Preset("foo")
    preset = Preset("bar", inherits=base_preset)
    assert len(preset.base_presets) == 1
    assert preset.base_presets[0].preset_name == base_preset.preset_name


def test_set_preset_multiple_base_presets_via_ctor():
    base_preset_1 = Preset("foo")
    base_preset_2 = Preset("bar")
    preset = Preset("baz", inherits=[base_preset_1, base_preset_2])
    assert len(preset.base_presets) == 2
    # Order matters - presets should be stored in the order they were added
    assert preset.base_presets[0].preset_name == base_preset_1.preset_name
    assert preset.base_presets[1].preset_name == base_preset_2.preset_name


def test_set_preset_single_base_preset_via_method():
    base_preset = Preset("foo")
    preset = Preset("bar")
    preset.inherit_from(base_preset)
    assert len(preset.base_presets) == 1
    assert preset.base_presets[0].preset_name == base_preset.preset_name


def test_set_preset_multiple_base_presets_via_method():
    base_preset_1 = Preset("foo")
    base_preset_2 = Preset("bar")
    preset = Preset("baz")
    preset.inherit_from(base_preset_1)
    preset.inherit_from(base_preset_2)
    assert len(preset.base_presets) == 2
    # Order matters - presets should be stored in the order they were added
    assert preset.base_presets[0].preset_name == base_preset_1.preset_name
    assert preset.base_presets[1].preset_name == base_preset_2.preset_name


def test_get_default_cmake_build_type():
    preset = Preset("foo")
    assert not preset.cmake_build_type


def test_get_built_in_cmake_build_type():
    build_type = ECMakeBuildType.MinSizeRel
    preset = Preset("foo")
    preset.cmake_build_type = build_type
    assert preset.cmake_build_type == build_type.value


def test_get_custom_cmake_build_type():
    build_type = "foo"
    preset = Preset("foo")
    preset.cmake_build_type = build_type
    assert preset.cmake_build_type == build_type


def test_clear_description():
    preset = Preset("foo")
    preset.description = "foo"
    assert preset.description == "foo"
    preset.description = None
    assert not preset.description


def test_clear_generator():
    preset = Preset("foo")
    preset.generator = ECMakeGenerator.Ninja
    assert preset.generator == ECMakeGenerator.Ninja.value
    preset.generator = None
    assert not preset.generator


def test_clear_binary_dir():
    preset = Preset("foo")
    preset.binary_dir = "foo"
    assert preset.binary_dir == "foo"
    preset.binary_dir = None
    assert not preset.binary_dir


def test_clear_install_dir():
    preset = Preset("foo")
    preset.install_dir = "foo"
    assert preset.install_dir == "foo"
    preset.install_dir = None
    assert not preset.install_dir


def test_clear_cache_variable():
    preset = Preset("foo")
    preset.set_cache_variable("foo", "bar")
    assert preset.cache_variables == {"foo": "bar"}
    preset.set_cache_variable("foo", None)
    assert not preset.cache_variables


def test_clear_env_variable():
    preset = Preset("foo")
    preset.set_env_variable("foo", "bar")
    assert preset.env_variables == {"foo": "bar"}
    preset.set_env_variable("foo", None)
    assert not preset.env_variables


def test_clear_build_type():
    preset = Preset("foo")
    preset.cmake_build_type = ECMakeBuildType.MinSizeRel
    assert preset.cmake_build_type == ECMakeBuildType.MinSizeRel.value
    preset.cmake_build_type = None
    assert not preset.cmake_build_type


def test_convert_to_build_preset_with_optional_fields_set():
    # Set up the preset
    preset = Preset("foo")
    preset.description = "foo"
    preset.generator = ECMakeGenerator.Ninja
    preset.hidden = True
    preset.binary_dir = "foo"
    preset.install_dir = "foo"
    preset.set_cache_variable("foo", "bar")
    preset.set_env_variable("foo", "bar")
    preset.cmake_build_type = ECMakeBuildType.MinSizeRel
    preset.inherit_from(Preset("bar"))
    preset.inherit_from(Preset("baz"))

    # Check the values written to the build preset dict
    build_preset = preset.as_build_preset(Path("/source"), Path("/generated"))
    assert build_preset["name"] == preset.preset_name
    assert build_preset["description"] == preset.description
    assert build_preset["hidden"]
    assert build_preset["configurePreset"] == preset.preset_name


def test_convert_to_build_preset_with_optional_fields_not_set():
    # Set up the preset
    preset = Preset("foo")

    # Check the values written to the build preset dict
    build_preset = preset.as_build_preset(Path("/source"), Path("/generated"))
    assert build_preset["name"] == preset.preset_name
    assert "description" not in build_preset
    assert "hidden" not in build_preset
    assert build_preset["configurePreset"] == preset.preset_name


def test_convert_to_configure_preset_with_optional_fields_set():
    # Set up the preset
    preset = Preset("foo")
    preset.description = "foo"
    preset.generator = ECMakeGenerator.Ninja
    preset.hidden = True
    preset.binary_dir = "foo"
    preset.install_dir = "foo"
    preset.set_cache_variable("foo", "bar")
    preset.set_env_variable("foo", "bar")
    preset.cmake_build_type = ECMakeBuildType.MinSizeRel
    preset.inherit_from(Preset("bar"))
    preset.inherit_from(Preset("baz"))

    # Check the values written to the configure preset dict
    configure_preset = preset.as_configure_preset(Path("/source"), Path("/generated"))
    assert configure_preset["name"] == preset.preset_name
    assert configure_preset["description"] == preset.description
    assert configure_preset["hidden"]
    assert configure_preset["generator"] == preset.generator
    assert configure_preset["binaryDir"] == str(Path("/source") / preset.binary_dir)
    assert configure_preset["installDir"] == str(Path("/source") / preset.install_dir)
    assert configure_preset["cacheVariables"] == preset.cache_variables
    assert configure_preset["environment"] == preset.env_variables
    assert configure_preset["inherits"] == [p.preset_name for p in preset.base_presets]


def test_preset_values_do_not_include_inherited_values():
    # Set up the preset
    base_preset = Preset("base")
    base_preset.cmake_build_type = ECMakeBuildType.MinSizeRel
    derived_preset = Preset("derived")
    derived_preset.inherit_from(base_preset)

    # Presets should not include inherited values unless they've been converted
    #   to a full preset
    assert not derived_preset.cmake_build_type


def test_full_preset_contains_inherited_values():
    # Set up the base preset but only with fields that should be inherited
    base_preset = Preset("base")
    base_preset.generator = ECMakeGenerator.Ninja
    base_preset.binary_dir = "foo"
    base_preset.install_dir = "bar"
    base_preset.cmake_build_type = ECMakeBuildType.MinSizeRel
    base_preset.set_env_variable("foo", "bar")

    derived_preset = Preset("derived")
    derived_preset.inherit_from(base_preset)

    # Full presets should include inherited values
    full_preset = derived_preset.as_full_preset()
    assert full_preset.generator == base_preset.generator
    assert full_preset.binary_dir == base_preset.binary_dir
    assert full_preset.install_dir == base_preset.install_dir
    assert full_preset.cmake_build_type == base_preset.cmake_build_type
    assert full_preset.env_variables == base_preset.env_variables


def test_full_preset_contains_inherited_values_from_multiple_bases():
    # Set up the presets
    base_preset_1 = Preset("base_1")
    base_preset_1.cmake_build_type = ECMakeBuildType.MinSizeRel
    base_preset_2 = Preset("base_2")
    base_preset_2.generator = ECMakeGenerator.Ninja
    derived_preset = Preset("derived")
    derived_preset.inherit_from(base_preset_1)
    derived_preset.inherit_from(base_preset_2)

    # Full presets should include inherited values from all bases
    full_preset = derived_preset.as_full_preset()
    assert full_preset.cmake_build_type == base_preset_1.cmake_build_type
    assert full_preset.generator == base_preset_2.generator


def test_later_bases_have_precedence_over_earlier_bases():
    # Set up the presets
    base_preset_1 = Preset("base_1")
    base_preset_1.cmake_build_type = ECMakeBuildType.MinSizeRel
    base_preset_2 = Preset("base_2")
    base_preset_2.cmake_build_type = ECMakeBuildType.Debug
    derived_preset = Preset("derived")
    derived_preset.inherit_from(base_preset_1)
    derived_preset.inherit_from(base_preset_2)

    # Full presets should include inherited values from all bases
    full_preset = derived_preset.as_full_preset()
    assert full_preset.cmake_build_type == base_preset_2.cmake_build_type


def test_configure_preset_does_not_contain_inherited_values():
    # Set up the presets
    base_preset = Preset("base")
    base_preset.generator = ECMakeGenerator.Ninja
    derived_preset = Preset("derived")
    derived_preset.inherit_from(base_preset)

    # The dictionary containing a CMake configure preset should not include
    #   inherited values since it contains an inherited block
    configure_preset = derived_preset.as_configure_preset(
        Path("/source"),
        Path("/generated")
    )
    assert "generator" not in configure_preset


def test_description_does_not_get_inherited():
    # Set up the presets
    base_preset = Preset("base")
    base_preset.description = "foo"
    derived_preset = Preset("derived")
    derived_preset.inherit_from(base_preset)

    # `description` should not be inherited
    full_preset = derived_preset.as_full_preset()
    assert not full_preset.description


def test_hidden_does_not_get_inherited():
    # Set up the presets
    base_preset = Preset("base")
    base_preset.hidden = True
    derived_preset = Preset("derived")
    derived_preset.inherit_from(base_preset)

    # `hidden` should not be inherited
    full_preset = derived_preset.as_full_preset()
    assert not full_preset.hidden


def test_configure_preset_converts_relative_paths_to_absolute_paths():
    # Set up the preset
    preset = Preset("foo")
    preset.binary_dir = "foo"
    preset.install_dir = "bar"

    # Check the values written to the configure preset dict
    source_dir = Path("/source")
    generated_dir = Path("/generated")
    configure_preset = preset.as_configure_preset(
        source_dir,
        generated_dir
    )

    assert configure_preset["binaryDir"] == str(source_dir / preset.binary_dir)
    assert configure_preset["installDir"] == str(source_dir / preset.install_dir)


def test_configure_preset_leaves_absolute_paths_untouched():
    # Set up the preset
    preset = Preset("foo")
    preset.binary_dir = "/foo"
    preset.install_dir = "/bar"

    # Check the values written to the configure preset dict
    source_dir = Path("/source")
    generated_dir = Path("/generated")
    configure_preset = preset.as_configure_preset(
        source_dir,
        generated_dir
    )

    assert configure_preset["binaryDir"] == preset.binary_dir
    assert configure_preset["installDir"] == preset.install_dir


def test_trace_file_generation(tmp_path: Any):
    # Constants used by the preset
    preset_name = "IS_A_PRESET"
    description = "foo"
    preset_generator = "MAYBE_A_GENERATOR"
    binary_dir = "/to/binary/dir"
    install_dir = "/to/install/dir"
    build_type = "COULD_BE_A_BUILD_TYPE"
    env_var_key = "abc"
    env_var_value = "def"
    base_preset_name = "base"

    # Set up the preset
    preset = Preset(preset_name)
    preset.description = description
    preset.hidden = True
    preset.generator = preset_generator
    preset.binary_dir = binary_dir
    preset.install_dir = install_dir
    preset.cmake_build_type = build_type
    preset.set_env_variable(env_var_key, env_var_value)
    preset.inherit_from(Preset(base_preset_name))

    # Generate the trace file
    generator = YamlFileGenerator()
    output_file = tmp_path / "preset.yml"
    preset.generate_trace_file(output_file, generator)

    # Check the contents of the trace file
    with open(output_file, "r") as f:
        contents = f.read()

    assert preset_name in contents
    assert description in contents
    assert preset_generator in contents
    assert binary_dir in contents
    assert install_dir in contents
    assert build_type in contents
    assert env_var_key in contents
    assert env_var_value in contents
    assert base_preset_name in contents
