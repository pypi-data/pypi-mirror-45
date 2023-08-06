import collections
from queue import Queue


def compress(data, node_delimiter=".", list_delimiter="/"):
    """
      Turn normal dict into flat with BFS-like queue
    :param data: dict to update
    :param node_delimiter: delimiter which split keys to nodes. For example:
      `{ 'mongo': { 'is': { 'awesome': True } } }` -> `{ 'mongo__is__awesome': True }`
    :param list_delimiter: delimiter which split keys to nodes and list indexes. For example:
      `{ 'mongo': ['is', 'awesome'] }` -> `{ 'mongo*0': 'is', 'mongo*1': 'awesome' }`
    :return: flat dict
    """

    if not isinstance(data, collections.Mapping):
        raise TypeError("Root data must have `dict` type")

    _flat = {}
    _queue = Queue()
    _queue.put(("", data))

    while not _queue.empty():
        _parent_name, _data = _queue.get()

        if isinstance(_data, collections.Mapping) and len(_data):
            for key, value in _data.items():
                _name = f"{_parent_name}{node_delimiter}" if _parent_name else ""

                _queue.put((f"{_name}{key}", value))

        elif isinstance(_data, (tuple, list)) and len(_data):
            for index, value in enumerate(_data):
                _queue.put((f"{_parent_name}{list_delimiter}{index}", value))
        else:
            _flat[f"{_parent_name}"] = _data

    return _flat


def _update_tree(parent, nodes, value, list_delimiter):
    # closure for simple access to parent[index] without return node
    def _initialize_node(index_or_key, type):
        try:
            parent[index_or_key]

        except IndexError:
            # parent is list but element with index does not exist
            parent.append(type())
            _initialize_node(index_or_key, type)

        except KeyError:
            # parent is list but element does not exist
            parent[index_or_key] = type()

    _head, *_tail = nodes

    _indexes = []

    if list_delimiter in _head:
        _head, *_indexes = _head.split(list_delimiter)

    # convert to int for _initialize_node -> parent[index_or_key]
    _indexes = [int(_index) for _index in _indexes]

    # is nested arrays or array
    if _indexes:
        _initialize_node(_head, list)

        parent = parent[_head]

        for i, _index in enumerate(_indexes):
            # is nested arrays
            if i < len(_indexes) - 1:
                _initialize_node(_index, list)
                parent = parent[_index]

            # is final value
            elif not _tail:
                _initialize_node(_index, lambda: value)
            else:
                _initialize_node(_index, dict)
                _update_tree(parent[_index], _tail, value, list_delimiter)

    # is nested dict
    elif _tail:
        _initialize_node(_head, dict)
        _update_tree(parent[_head], _tail, value, list_delimiter)

    # is final value
    else:
        parent[_head] = value
        return


def expand(data, node_delimiter: str = ".", list_delimiter: str = "/"):
    """
      Turn flat dict into normal
    :param data: dict with flat keys
    :param node_delimiter: delimiter which split keys to nodes. For example:
      `{ 'mongo__is__awesome': True }` -> `{ 'mongo': { 'is': { 'awesome': True } } }`
    :param list_delimiter: delimiter which split keys to nodes and list indexes. For example:
      `{ 'mongo*0': 'is', 'mongo*1': 'awesome' }` -> `{ 'mongo': ['is', 'awesome'] }`
    :return: updated dict
    """
    if not isinstance(data, collections.Mapping):
        raise TypeError("Root data must have `Mapping` type")

    _tree = {}

    for _key, _value in data.items():
        _nodes = _key.split(node_delimiter)
        _update_tree(_tree, _nodes, _value, list_delimiter)

    return _tree


__all__ = [
    'compress',
    'expand'
]
