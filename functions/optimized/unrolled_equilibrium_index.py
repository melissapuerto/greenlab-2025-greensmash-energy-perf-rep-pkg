"""
Optimized (Loop-Unrolled x4) Equilibrium Index — scaled input (Option 1: 973075 elements).
Reference: https://www.geeksforgeeks.org/equilibrium-index-of-an-array/
"""

from __future__ import annotations
import random
import time


def equilibrium_index(arr: list[int]) -> int:
    n = len(arr)
    total_sum = sum(arr)
    left_sum = 0
    i = 0

    # Loop unrolled by 4
    while i <= n - 4:
        # iteration 1
        total_sum -= arr[i]
        if left_sum == total_sum:
            return i
        left_sum += arr[i]

        # iteration 2
        total_sum -= arr[i + 1]
        if left_sum == total_sum:
            return i + 1
        left_sum += arr[i + 1]

        # iteration 3
        total_sum -= arr[i + 2]
        if left_sum == total_sum:
            return i + 2
        left_sum += arr[i + 2]

        # iteration 4
        total_sum -= arr[i + 3]
        if left_sum == total_sum:
            return i + 3
        left_sum += arr[i + 3]

        i += 4

    # leftover elements
    while i < n:
        total_sum -= arr[i]
        if left_sum == total_sum:
            return i
        left_sum += arr[i]
        i += 1

    return -1


if __name__ == "__main__":
    NUM_ELEMENTS = 973075  # Option 1: large input
    # Generate a large array with integer values
    arr = [random.randint(-100, 100) for _ in range(NUM_ELEMENTS)]

    start = time.time()
    idx = equilibrium_index(arr)
    end = time.time()

    print(f"Equilibrium index: {idx}")
    print(f"Array size: {NUM_ELEMENTS}")
    print(f"Execution time: {end - start:.2f} s")
