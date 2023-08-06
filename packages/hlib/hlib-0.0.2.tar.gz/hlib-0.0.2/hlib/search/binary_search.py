from typing import Callable, Sequence, TypeVar


T = TypeVar('T')

def binary_search(arr: Sequence[T], target: T, comp: Callable[[T, T], bool]=lambda x, y: x < y) -> int:
    start = 0
    end = len(arr) - 1
    while start <= end:
        mid = (start + end) // 2
        if arr[mid] == target:
            return mid
        else:
            if comp(arr[mid], target):
                start = mid + 1
            else:
                end = mid - 1
    
    return -1
