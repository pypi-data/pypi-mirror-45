from typing import Callable, Sequence, TypeVar


T = TypeVar('T')

def mergesort(arr: Sequence[T], comp: Callable[[T, T], bool]=lambda x, y: x < y):
    return _mergesort(arr, comp)

def _mergesort(arr: Sequence[T], comp: Callable[[T, T], bool]):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = _mergesort(arr[:mid], comp)
    right = _mergesort(arr[mid:], comp)

    return _merge(left, right, comp)

def _merge(left: int, right: int, comp: Callable[[T, T], bool]):
    merge = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if comp(left[i], right[j]):
            merge.append(left[i])
            i += 1
        else:
            merge.append(right[j])
            j += 1

    while i  < len(left):
        merge.append(left[i])
        i += 1

    while j < len(right):
        merge.append(right[j])
        j += 1

    return merge