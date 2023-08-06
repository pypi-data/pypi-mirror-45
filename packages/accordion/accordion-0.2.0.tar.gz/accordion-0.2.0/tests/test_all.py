from unittest import TestCase

from accordion import compress, expand


class FlatTestCase(TestCase):
    def test_compress(self):
        _compressed = {"data__item*0": 1, "data__item*1": 2, "data__item*2": 3}
        _ex_normal = compress({"data": {"item": [1, 2, 3]}}, node_delimiter="__", list_delimiter="*")
        assert _compressed == _ex_normal

    def test_expand(self):
        _compressed = {"data__item*0": 1, "data__item*1": 2, "data__item*2": 3}
        _normal = {"data": {"item": [1, 2, 3]}}
        _ex_compressed = expand(_compressed, node_delimiter="__", list_delimiter="*")
        assert _normal == _ex_compressed

    def test_both(self):
        _source = {"data": {"item": [1, 2, 3]}}
        _modified = compress(_source, node_delimiter="__", list_delimiter="*")
        _like_source = expand(_modified, node_delimiter="__", list_delimiter="*")
        assert _source == _like_source

    def test_empty(self):
        _source = {"data": {"item": []}}
        _modified = compress(_source)
        _like_source = expand(_modified)
        assert _source == _like_source

    def test_matrix(self):
        _source = {
            'matrix/0/0': 1,
            'matrix/0/1': 2,
            'matrix/0/2': 3,

            'matrix/1/0': 4,
            'matrix/1/1': 5,
            'matrix/1/2': 6,

            'matrix/2/0': 7,
            'matrix/2/1': 8,
            'matrix/2/2': 9,
        }

        assert expand(_source) == {
            'matrix': [
                [1, 2, 3],
                [4, 5, 6],
                [7, 8, 9]
            ]
        }
