from pymake.common.scope import EScope
from pymake.core.scoped_sets import ScopedSets
from typing import Any

def test_scoped_sets_empty_after_construction():
    scoped_sets: ScopedSets[str] = ScopedSets()
    assert not scoped_sets


def test_scoped_sets_not_empty_after_adding_to_public():
    scoped_sets: ScopedSets[str] = ScopedSets()
    scoped_sets.public.add("foo")
    assert scoped_sets


def test_scoped_sets_not_empty_after_adding_to_interface():
    scoped_sets: ScopedSets[str] = ScopedSets()
    scoped_sets.interface.add("foo")
    assert scoped_sets


def test_scoped_sets_not_empty_after_adding_to_private():
    scoped_sets: ScopedSets[str] = ScopedSets()
    scoped_sets.private.add("foo")
    assert scoped_sets


def test_select_public_set():
    scoped_sets: ScopedSets[str] = ScopedSets()
    assert scoped_sets.select_set(EScope.PUBLIC) is scoped_sets.public


def test_select_interface_set():
    scoped_sets: ScopedSets[str] = ScopedSets()
    assert scoped_sets.select_set(EScope.INTERFACE) is scoped_sets.interface


def test_select_private_set():
    scoped_sets: ScopedSets[str] = ScopedSets()
    assert scoped_sets.select_set(EScope.PRIVATE) is scoped_sets.private


def test_trace_dict_contains_all_values():
    public_val = "foo"
    interface_val = "bar"
    private_val = "baz"

    # Set up the scoped sets
    scoped_sets: ScopedSets[str] = ScopedSets()
    scoped_sets.public.add(public_val)
    scoped_sets.interface.add(interface_val)
    scoped_sets.private.add(private_val)

    # These are the keys that should exist regardless of what the scoped set
    #   contains
    trace_dict = scoped_sets.to_trace_dict()
    assert "public" in trace_dict
    assert "interface" in trace_dict
    assert "private" in trace_dict

    # Check if the added values are in the trace dict and in the correct set
    public_values: Any = trace_dict["public"]
    interface_values: Any = trace_dict["interface"]
    private_values: Any = trace_dict["private"]

    # Each dictionary will be instances of Traced objects. Rather than try and
    #   extract the value from the Traced object, just check if the value is
    #   in the string representation of the dictionary.
    assert public_val in str(public_values)
    assert interface_val in str(interface_values)
    assert private_val in str(private_values)


def test_merge_sets():
    public_val = "foo"
    interface_val = "bar"
    private_val = "baz"

    # Set up the scoped sets
    scoped_sets: ScopedSets[str] = ScopedSets()
    scoped_sets.public.add(public_val)
    scoped_sets.interface.add(interface_val)
    scoped_sets.private.add(private_val)

    # Merge the sets
    other_scoped_sets: ScopedSets[str] = ScopedSets()
    other_scoped_sets.public.add("other_public")
    other_scoped_sets.interface.add("other_interface")
    other_scoped_sets.private.add("other_private")
    scoped_sets.merge(other_scoped_sets)

    # Check that the values from the other set are in the current set
    assert public_val in scoped_sets.public
    assert interface_val in scoped_sets.interface
    assert private_val in scoped_sets.private
    assert "other_public" in scoped_sets.public
    assert "other_interface" in scoped_sets.interface
    assert "other_private" not in scoped_sets.private


def test_merge_sets_including_private_values():
    public_val = "foo"
    interface_val = "bar"
    private_val = "baz"

    # Set up the scoped sets
    scoped_sets: ScopedSets[str] = ScopedSets()
    scoped_sets.public.add(public_val)
    scoped_sets.interface.add(interface_val)
    scoped_sets.private.add(private_val)

    # Merge the sets
    other_scoped_sets: ScopedSets[str] = ScopedSets()
    other_scoped_sets.public.add("other_public")
    other_scoped_sets.interface.add("other_interface")
    other_scoped_sets.private.add("other_private")
    scoped_sets.merge(other_scoped_sets, merge_private=True)

    # Check that the values from the other set are in the current set
    assert public_val in scoped_sets.public
    assert interface_val in scoped_sets.interface
    assert private_val in scoped_sets.private
    assert "other_public" in scoped_sets.public
    assert "other_interface" in scoped_sets.interface
    assert "other_private" in scoped_sets.private
