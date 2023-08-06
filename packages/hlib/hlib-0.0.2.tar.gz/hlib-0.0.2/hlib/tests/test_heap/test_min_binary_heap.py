import unittest

from heap.min_binary_heap import MinBinaryHeap


class TestStack(unittest.TestCase):
    def setUp(self): 
        self.heap = MinBinaryHeap[int]()

    def test_push(self):
        self.heap.push(0)
        self.assertEqual(self.heap.peek(), 0)
        self.heap.push(-1)
        self.assertEqual(self.heap.peek(), -1)
        self.heap.push(-2)
        self.assertEqual(self.heap.peek(), -2)
        self.heap.push(1)
        self.assertEqual(self.heap.peek(), -2)
        self.heap.push(-3)
        self.assertEqual(self.heap.peek(), -3)
        self.heap.push(-4)
        self.assertEqual(self.heap.peek(), -4)
        self.heap.push(7)
        self.assertEqual(self.heap.peek(), -4)

    def test_push_increasing(self):
        inputs = range(0, 7)
        for i in inputs:
            self.heap.push(i)
            self.assertEqual(self.heap.peek(), inputs[0])

    def test_push_decreasing(self):
        for i in range(7, -1, -1):
            self.heap.push(i)
            self.assertEqual(self.heap.peek(), i)

    def test_pop(self):
        inputs = [0, -1, -2, 1, -3, -4, 7]
        for i in inputs:
            self.heap.push(i)
          
        for i in sorted(inputs):
            self.assertEqual(self.heap.pop(), i)

    def test_pop_increasing(self):
        inputs = range(0, 7)
        for i in inputs:
            self.heap.push(i)

        for i in inputs:
            self.assertEqual(self.heap.pop(), i)

    def test_pop_decreasing(self):
        inputs = range(7, -1, -1)
        for i in inputs:
            self.heap.push(i)

        for i in reversed(inputs):
            self.assertEqual(self.heap.pop(), i)

    def test_pop_empty(self):
        self.assertRaises(Exception, self.heap.pop)

    def test_pop_single(self):
        self.heap.push(1)
        self.assertEqual(self.heap.pop(), 1)
        self.assertRaises(Exception, self.heap.pop)

    def test_peek(self):
        self.heap.push(1)
        self.assertEqual(self.heap.peek(), 1)
        self.heap.push(-1)
        self.assertEqual(self.heap.peek(), -1)
        self.heap.push(0)
        self.assertEqual(self.heap.peek(), -1)

    def test_peek_empty(self):
        self.assertRaises(Exception, self.heap.peek)
  
    def test_is_empty_true(self):
        self.assertEqual(self.heap.is_empty(), True)

    def test_is_empty_false(self):
        self.heap.push(1)
        self.assertEqual(self.heap.is_empty(), False)
