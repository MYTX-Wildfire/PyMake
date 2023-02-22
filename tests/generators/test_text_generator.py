from pymake.generators.text_generator import TextGenerator
import pytest

def test_at_start_of_line_when_newly_constructed():
    generator = TextGenerator()
    assert generator.at_start_of_line


def test_at_start_of_line_after_partially_adding_line():
    generator = TextGenerator()
    generator.append("foo")
    assert not generator.at_start_of_line


def test_at_start_of_line_after_fully_adding_line():
    generator = TextGenerator()
    generator.append_line("foo")
    assert generator.at_start_of_line


def test_initial_indentation_level():
    generator = TextGenerator()
    assert generator.indentation_level == 0


def test_initial_text():
    generator = TextGenerator()
    assert generator.text == ""


def test_append():
    generator = TextGenerator()
    generator.append("foo")
    assert generator.text == "foo"


def test_append_line():
    generator = TextGenerator()
    generator.append_line("foo")
    assert generator.text == "foo\n"


def test_apply_zero_indentation():
    generator = TextGenerator()
    generator.apply_indentation()
    generator.append("foo")
    assert generator.text == "foo"


def test_apply_indentation_using_tabs():
    generator = TextGenerator()
    generator.indentation_level = 1
    generator.apply_indentation()
    generator.append("foo")
    assert generator.text == "\tfoo"


def test_apply_indentation_using_spaces():
    generator = TextGenerator(use_spaces=True, tab_size=4)
    generator.indentation_level = 1
    generator.apply_indentation()
    generator.append("foo")
    assert generator.text == "    foo"


def test_apply_multiple_indentation_levels_using_tabs():
    generator = TextGenerator()
    generator.indentation_level = 2
    generator.apply_indentation()
    generator.append("foo")
    assert generator.text == "\t\tfoo"


def test_apply_multiple_indentation_levels_using_spaces():
    generator = TextGenerator(use_spaces=True, tab_size=4)
    generator.indentation_level = 2
    generator.apply_indentation()
    generator.append("foo")
    assert generator.text == "        foo"


def test_remove_last_instance_of_nonexistent_string():
    generator = TextGenerator()
    generator.append("foo")
    generator.remove_last_instance_of("bar")
    assert generator.text == "foo"


def test_remove_last_instance_of_existing_string():
    generator = TextGenerator()
    generator.append("foo")
    generator.remove_last_instance_of("foo")
    assert generator.text == ""


def test_remove_last_instance_of_existing_string_with_multiple_instances():
    generator = TextGenerator()
    generator.append("foo")
    generator.append("bar")
    generator.append("foo")
    generator.remove_last_instance_of("foo")
    assert generator.text == "foobar"


def test_increase_indentation_level():
    generator = TextGenerator()
    generator.append_line("foo")
    generator.increase_indentation_level()
    generator.append_line("bar")
    assert generator.text == "foo\n\tbar\n"


def test_decrease_indentation_level():
    generator = TextGenerator()
    generator.increase_indentation_level()
    generator.append_line("foo")
    generator.decrease_indentation_level()
    generator.append_line("bar")
    assert generator.text == "\tfoo\nbar\n"


def test_modify_indentation_level():
    generator = TextGenerator()
    generator.append_line("foo")
    generator.modify_indentation_level(2)
    generator.append_line("bar")
    assert generator.text == "foo\n\t\tbar\n"


def test_modify_indentation_level_clamps_to_zero():
    generator = TextGenerator()
    generator.append_line("foo")
    generator.modify_indentation_level(-1)
    generator.append_line("bar")
    assert generator.text == "foo\nbar\n"


def test_set_indentation_level_throws_if_negative():
    generator = TextGenerator()
    with pytest.raises(ValueError):
        generator.indentation_level = -1


def test_finish_line_with_no_text_added():
    generator = TextGenerator()
    generator.finish_line()
    assert generator.text == ""


def test_finish_line_when_not_at_start_of_line():
    generator = TextGenerator()
    generator.append("foo")
    generator.finish_line()
    assert generator.text == "foo\n"


def test_finish_line_when_at_start_of_line():
    generator = TextGenerator()
    generator.append_line("foo")
    generator.finish_line()
    assert generator.text == "foo\n"
