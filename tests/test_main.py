import pytest

from hash_map import HashMap
from tests.point import Point


@pytest.mark.parametrize(
    "items,pairs_after_adding",
    [
        pytest.param([], [], id="empty dictionary should have len equal to 0"),
        pytest.param(
            [(1, "one"), (2, "two"), (3, "tree"), (4, "four")],
            [(1, "one"), (2, "two"), (3, "tree"), (4, "four")],
            id="integers can be used as keys",
        ),
        pytest.param(
            [(1.1, "one"), (2.2, "two"), (3.3, "tree"), (4.4, "four")],
            [(1.1, "one"), (2.2, "two"), (3.3, "tree"), (4.4, "four")],
            id="floats can be used as keys",
        ),
        pytest.param(
            [("one", 1), ("two", 2), ("tree", 3), ("four", 4)],
            [("one", 1), ("two", 2), ("tree", 3), ("four", 4)],
            id="strings can be used as keys",
        ),
        pytest.param(
            [
                (Point(0, 0), "origin"),
                (Point(10, 10), "A"),
                (Point(-10, 10), "B"),
                (Point(0, 5), "C"),
            ],
            [
                (Point(0, 0), "origin"),
                (Point(10, 10), "A"),
                (Point(-10, 10), "B"),
                (Point(0, 5), "C"),
            ],
            id="Custom hashable classes can be used as keys",
        ),
        pytest.param(
            [("one", 1), (2, [1, 2, 3]), (13.3, 66), (Point(0, 0), "origin")],
            [("one", 1), (2, [1, 2, 3]), (13.3, 66), (Point(0, 0), "origin")],
            id="keys can have different hashable types",
        ),
        pytest.param(
            [
                (8, "8"),
                (16, "16"),
                (32, "32"),
                (64, "64"),
                (128, "128"),
                ("one", 2),
                ("two", 2),
                (Point(1, 1), "a"),
                ("one", 1),
                ("one", 11),
                ("one", 111),
                ("one", 1111),
                (145, 146),
                (145, 145),
                (145, -1),
                ("two", 22),
                ("two", 222),
                ("two", 2222),
                ("two", 22222),
                (Point(1, 1), "A"),
            ],
            [
                (8, "8"),
                (16, "16"),
                (32, "32"),
                (64, "64"),
                (128, "128"),
                ("one", 1111),
                ("two", 22222),
                (145, -1),
                (Point(1, 1), "A"),
            ],
            id="the value should be reassigned when the key already exists",
        ),
    ],
)
def test_put_and_get_pairs(items: list, pairs_after_adding: list):

    hash_map = HashMap()
    for key, value in items:
        hash_map.put(key=key, value=value)

    for key, value in pairs_after_adding:
        assert hash_map.get(key=key) == value
    assert len(hash_map) == len(pairs_after_adding)


def test_delete_pairs():
    items = [(f"Element {i}", i) for i in range(1000)]
    hash_map = HashMap()
    for key, value in items:
        hash_map[key] = value
    for key, value in items:
        assert hash_map[key] == value
    assert len(hash_map) == len(items)
    for key, value in items:
        del hash_map[key]


def test_unhashable_key():
    hash_map = HashMap()
    with pytest.raises(TypeError):
        hash_map.put(key=[1, 2], value="some value")


def test_retrieving_non_existing_key():
    hash_map = HashMap()
    with pytest.raises(KeyError):
        print(hash_map[1])


def test_default_value():
    hash_map = HashMap()
    assert hash_map.get(1) is None
    assert hash_map.get(1, "custom value") == "custom value"


def test_trying_to_delete_non_existing_key():
    hash_map = HashMap()
    with pytest.raises(KeyError):
        del hash_map[1]


def test_resize_bucket_using_dict_assignment_syntax():
    items = [(f"Element {i}", i) for i in range(1000)]
    hash_map = HashMap()
    for key, value in items:
        hash_map[key] = value

    for key, value in items:
        assert hash_map[key] == value
    assert len(hash_map) == len(items)


def test_create_from_iterable():
    hash_map = HashMap(iterable=[(1, "one"), (2, "two")])
    assert hash_map[1] == "one"
    assert hash_map.get(2) == "two"
