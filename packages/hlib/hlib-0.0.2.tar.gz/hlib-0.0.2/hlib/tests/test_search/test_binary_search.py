import unittest

from search.binary_search import binary_search


class TestStack(unittest.TestCase):
    def test_search_empty(self):
        inputs = []
        self.assertEqual(-1, binary_search(inputs, 42))

    def test_search_single(self):
        inputs = [42]
        self.assertEqual(0, binary_search(inputs, 42))

    def test_search_single_missing(self):
        inputs = [42]
        self.assertEqual(-1, binary_search(inputs, 1))

    def test_search_even(self):
        inputs = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89]
        self.assertEqual(3, binary_search(inputs, 7))
        self.assertEqual(13, binary_search(inputs, 43))
        self.assertEqual(21, binary_search(inputs, 79))

    def test_search_even_missing(self):
        inputs = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89]
        self.assertEqual(-1, binary_search(inputs, -42))

    def test_search_even_edges(self):
        inputs = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89]
        self.assertEqual(0, binary_search(inputs, 2))
        self.assertEqual(23, binary_search(inputs, 89))

    def test_search_odd(self):
        inputs = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        self.assertEqual(3, binary_search(inputs, 7))
        self.assertEqual(13, binary_search(inputs, 43))
        self.assertEqual(21, binary_search(inputs, 79))

    def test_search_odd_missing(self):
        inputs = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        self.assertEqual(-1, binary_search(inputs, -42))

    def test_search_odd_edges(self):
        inputs = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        self.assertEqual(0, binary_search(inputs, 2))
        self.assertEqual(24, binary_search(inputs, 97))