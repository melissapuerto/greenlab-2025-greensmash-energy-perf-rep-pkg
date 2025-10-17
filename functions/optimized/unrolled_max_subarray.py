"""
Unrolled (x4) Divide-and-Conquer Maximum Subarray
Option 1: Increased input size to 973,075 for energy profiling.
"""

from __future__ import annotations
import random
import time
from collections.abc import Sequence


def unroll4_max_subarray(
    arr: Sequence[float], low: int, high: int
) -> tuple[int | None, int | None, float]:
    if not arr:
        return None, None, 0
    if low == high:
        return low, high, arr[low]

    mid = (low + high) // 2
    left_low, left_high, left_sum = unroll4_max_subarray(arr, low, mid)
    right_low, right_high, right_sum = unroll4_max_subarray(arr, mid + 1, high)
    cross_left, cross_right, cross_sum = unroll4_max_cross_sum(arr, low, mid, high)

    if left_sum >= right_sum and left_sum >= cross_sum:
        return left_low, left_high, left_sum
    elif right_sum >= left_sum and right_sum >= cross_sum:
        return right_low, right_high, right_sum
    else:
        return cross_left, cross_right, cross_sum


def unroll4_max_cross_sum(
    arr: Sequence[float], low: int, mid: int, high: int
) -> tuple[int, int, float]:
    left_sum = float("-inf")
    right_sum = float("-inf")
    max_left = -1
    max_right = -1

    # ---------- LEFT SIDE ----------
    summ = 0
    i = mid
    while i - 3 >= low:
        for j in (i, i - 1, i - 2, i - 3):
            summ += arr[j]
            if summ > left_sum:
                left_sum = summ
                max_left = j
        i -= 4

    while i >= low:
        summ += arr[i]
        if summ > left_sum:
            left_sum = summ
            max_left = i
        i -= 1

    # ---------- RIGHT SIDE ----------
    summ = 0
    i = mid + 1
    while i + 3 <= high:
        for j in (i, i + 1, i + 2, i + 3):
            summ += arr[j]
            if summ > right_sum:
                right_sum = summ
                max_right = j
        i += 4

    while i <= high:
        summ += arr[i]
        if summ > right_sum:
            right_sum = summ
            max_right = i
        i += 1

    return max_left, max_right, left_sum + right_sum


if __name__ == "__main__":
    NUM_ELEMENTS = 973075  # Option 1: large input
    arr = [random.randint(-100, 100) for _ in range(NUM_ELEMENTS)]

    start = time.time()
    result = unroll4_max_subarray(arr, 0, NUM_ELEMENTS - 1)
    end = time.time()

    print(f"Max subarray result: {result}")
    print(f"Array size: {NUM_ELEMENTS}")
    print(f"Execution time: {end - start:.2f} seconds")
