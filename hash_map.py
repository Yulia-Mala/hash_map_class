from dataclasses import dataclass
from typing import Hashable, Any, Iterable, Generator


@dataclass
class Node:
    key_hash: int
    key: Hashable
    value: Any
    deleted = False


class HashMap:
    MIN_SIZE = 8
    LOAD_FACTOR = 0.65

    def __init__(self, iterable: Iterable = (), ) -> None:
        self.capacity = (max(self.MIN_SIZE, len([iterable]) * 2))
        self.content = [None] * self.capacity
        self.length = 0
        if iterable:
            try:
                self._add_from_iterable(iterable)
            except TypeError as error:
                raise TypeError(f"Please provide iterable to create hashmap in such a format:"
                                f"((key1, value1), (key2, value2), ...) "
                                f"original error's text: {str(error)}")

    def __len__(self) -> int:
        return self.length

    def __iter__(self) -> Iterable:
        return iter(
            [(node.key, node.value) for node in self._get_real_nodes()]
        )

    def __str__(self) -> str:
        return "\n".join(
            [f"key {node.key}: value {node.value}" for node in self._get_real_nodes()]
        )

    def __setitem__(self, key: Hashable, value: Any) -> None:
        """ I used open addressing to handle the collisions like python built-in dict do it.
        It's also possible to use chaining. I keep Nodes directly in self.content attribute"""
        if self.capacity * self.LOAD_FACTOR < len(self) + 1:
            self._resize()

        for index, node_link in self._indices_generator(key):
            if node_link is None or node_link.deleted:
                self.content[index] = (Node(key_hash=hash(key), key=key, value=value))
                self.length += 1
                break
            if hash(key) == node_link.key_hash and node_link.key == key:
                node_link.value = value
                break

    def __getitem__(self, key: Hashable) -> Any:
        for index, node_link in self._indices_generator(key):
            if node_link is None:
                raise KeyError(f"{key} key doesn't exist in this HashMap")
            if hash(key) == node_link.key_hash and node_link.key == key:
                return node_link.value

    def __delitem__(self, key: Hashable) -> None:
        """ this method allow to delete pair using syntax: del hashmap_name[key] """
        for index, node_link in self._indices_generator(key):
            if node_link is None:
                raise KeyError(
                    f"key / {key} / you want to delete doesn't exist in this HashMap"
                )
            if hash(key) == node_link.key_hash and node_link.key == key:
                node_link.deleted = True
                self.length -= 1
                break

    def _add_from_iterable(self, iterable: Iterable) -> None:
        for key, value in iterable:
            self.__setitem__(key, value)

    def _get_real_nodes(self) -> list:
        return [node for node in self.content
                if isinstance(node, Node) and not node.deleted]

    def _indices_generator(self, key: Hashable) -> Generator:
        index = hash(key) % self.capacity
        while True:
            yield index, self.content[index]
            index = (index + 1) % self.capacity

    def _resize(self) -> None:
        self.length = 0
        self.capacity *= 2
        content_copy = self._get_real_nodes()
        self.content = [None] * self.capacity

        for node in content_copy:
            self.__setitem__(node.key, node.value)

    def get(self, key: Hashable, default: Any = None) -> Any:
        """ we could use python dict syntax with [] to get the key, in such a case we'd receive
        KeyError when trying to retrieve non-existing key.
        If we use get method we could specify default value or would receive None
        when trying to retrieve non-existing key."""
        try:
            value = self.__getitem__(key)
        except KeyError:
            value = default
        return value

    def put(self, key: Hashable, value: Any):
        self.__setitem__(key, value)

    def clear(self) -> None:
        self.content = [None] * self.capacity
        self.length = 0
