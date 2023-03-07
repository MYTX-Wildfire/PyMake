from pymake.tracing.traced_set import TracedSet

def test_is_empty_after_construction():
    xs: TracedSet[int] = TracedSet()
    assert not xs


def test_not_empty_after_adding_value():
    xs: TracedSet[int] = TracedSet()
    xs.add(1)
    assert xs


def test_traced_set_contains_value():
    xs: TracedSet[int] = TracedSet()
    keys = [ 1, 2, 3 ]
    not_keys = [ 4, 5 ]

    for key in keys:
        xs.add(key)

    for key in keys:
        assert key in xs

    for key in not_keys:
        assert key not in xs


def test_iterate_over_values():
    xs: TracedSet[int] = TracedSet()
    keys = { 1, 2, 3 }
    for key in keys:
        xs.add(key)

    for x in xs:
        keys.remove(x.value)

    assert not keys


def test_clone_returns_new_instance():
    xs: TracedSet[int] = TracedSet()
    ys = xs.clone()
    assert xs is not ys
