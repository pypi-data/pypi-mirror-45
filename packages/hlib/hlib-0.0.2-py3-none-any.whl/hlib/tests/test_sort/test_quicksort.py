import unittest

from sort.quicksort import quicksort


class TestStack(unittest.TestCase):
    def test_sort_empty(self):
        inputs = []
        quicksort(inputs)
        self.assertEqual([], inputs)

    def test_sort_single(self):
        inputs = [42]
        quicksort(inputs)
        self.assertEqual([42], inputs)

    def test_sort(self):
        inputs = [9, 3, 83, 9, 2, 0, 1, 65, 2, 822, 9, 11, 22, 3, 3, 3, 47]
        quicksort(inputs)
        self.assertEqual([0, 1, 2, 2, 3, 3, 3, 3, 9, 9, 9, 11, 22, 47, 65, 83, 822], inputs)

    def test_sort_even(self):
        inputs = [-6, 9, 0, 1, 17, 91, 0, 178]
        quicksort(inputs)
        self.assertEqual([-6, 0, 0, 1, 9, 17, 91, 178], inputs)

    def test_sort_odd(self):
        inputs = [8, 2, 78, 892, 11, 0, 34]
        quicksort(inputs)
        self.assertEqual([0, 2, 8, 11, 34, 78, 892], inputs)

    def test_sort_increasing(self):
        inputs = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        quicksort(inputs)
        self.assertEqual([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], inputs)

    def test_sort_decreasing(self):
        inputs = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
        quicksort(inputs)
        self.assertEqual([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], inputs)
