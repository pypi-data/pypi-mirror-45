from typing import Generic, TypeVar

from heap.binary_heap import BinaryHeap


T = TypeVar('T')

class MaxBinaryHeap(Generic[T], BinaryHeap[T]):
    def __init__(self):
        super().__init__(lambda x, y: x > y)