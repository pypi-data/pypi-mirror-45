from typing import Callable, Sequence, TypeVar


T = TypeVar('T')

def quicksort(arr: Sequence[T], comp: Callable[[T, T], bool]=lambda x, y: x < y):
    _quicksort(arr, 0, len(arr) - 1, comp)

def _quicksort(arr: Sequence[T], start: int, end: int, comp: Callable[[T, T], bool]):
    if start < end:
        pivot = _partition(arr, start, end, comp)
        _quicksort(arr, start, pivot - 1, comp)
        _quicksort(arr, pivot + 1, end, comp)

def _partition(arr: Sequence[T], start: int, end: int, comp: Callable[[T, T], bool]):
    pivot = arr[end]
    i = start - 1
    for j in range(start, end):
        if comp(arr[j], pivot):
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i+1], arr[end] = arr[end], arr[i+1]
    return i + 1