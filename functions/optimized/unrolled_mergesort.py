# optimized/mergesort.py: loop unrolled 4
from __future__ import annotations
import random, time


def merge(left_half: list, right_half: list) -> list:
    sorted_array = [None] * (len(right_half) + len(left_half))
    pointer1 = 0
    pointer2 = 0
    index = 0
    len_left = len(left_half)
    len_right = len(right_half)

    # Loop unrolling by 4 elements
    while pointer1 + 3 < len_left and pointer2 + 3 < len_right:
        for _ in range(4):
            if left_half[pointer1] < right_half[pointer2]:
                sorted_array[index] = left_half[pointer1]
                pointer1 += 1
            else:
                sorted_array[index] = right_half[pointer2]
                pointer2 += 1
            index += 1

    # Handle remaining elements normally
    while pointer1 < len_left and pointer2 < len_right:
        if left_half[pointer1] < right_half[pointer2]:
            sorted_array[index] = left_half[pointer1]
            pointer1 += 1
        else:
            sorted_array[index] = right_half[pointer2]
            pointer2 += 1
        index += 1

    while pointer1 < len_left:
        sorted_array[index] = left_half[pointer1]
        pointer1 += 1
        index += 1

    while pointer2 < len_right:
        sorted_array[index] = right_half[pointer2]
        pointer2 += 1
        index += 1

    return sorted_array


def merge_sort(array: list) -> list:
    if len(array) <= 1:
        return array
    middle = len(array) // 2
    return merge(merge_sort(array[:middle]), merge_sort(array[middle:]))


if __name__ == "__main__":
    INPUT_SIZE = 973075  # Option 1: scaled-up input
    arr = [random.randint(0, 1000000) for _ in range(INPUT_SIZE)]

    start = time.time()
    merge_sort(arr)
    end = time.time()

    print(f"Input size: {INPUT_SIZE}")
    print(f"Execution time: {end - start:.2f} seconds")
