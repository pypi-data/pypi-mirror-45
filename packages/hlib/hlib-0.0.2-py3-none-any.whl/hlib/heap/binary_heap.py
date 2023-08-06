from typing import Callable, Generic, TypeVar


T = TypeVar('T')

class BinaryHeap(Generic[T]):
    def __init__(self, comparator: Callable[[T, T], bool]):
        self._heap = [None]
        self._comparator = comparator

    def push(self, value: T):
        self._heap.append(value)
        self._bubble_up(len(self._heap) - 1)

    def pop(self):
        if self.is_empty():
            raise Exception

        self._heap[1], self._heap[len(self._heap) - 1] = self._heap[len(self._heap) - 1], self._heap[1]
        value = self._heap.pop()
        self._bubble_down(1)
        return value

    def peek(self):
        if self.is_empty():
            raise Exception

        return self._heap[1] 

    def is_empty(self):
        return len(self._heap) <= 1

    def _bubble_up(self, i: int):
        value = self._heap[i]
        while i // 2 > 0 and self._comparator(value, self._heap[i // 2]):
            self._heap[i], self._heap[i // 2] = self._heap[i // 2], self._heap[i]
            i = i // 2

    def _bubble_down(self, i: int):
        swap_index = i
        if i * 2 <= len(self._heap) - 1 and self._comparator(self._heap[i * 2], self._heap[swap_index]):
            swap_index = i * 2

        if i * 2 + 1 <= len(self._heap) - 1 and self._comparator(self._heap[i * 2 + 1], self._heap[swap_index]):
            swap_index = i * 2 + 1
        
        if swap_index != i:
          self._heap[i], self._heap[swap_index] = self._heap[swap_index], self._heap[i]
          self._bubble_down(swap_index)
