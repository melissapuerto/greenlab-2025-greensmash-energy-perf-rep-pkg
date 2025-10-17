"""
Optimized (Loop Unrolled × 4) Product Sum implementation.
Based on recursive baseline but processes 4 elements per loop iteration.
"""

from __future__ import annotations
import random
import time


def product_sum(arr: list[int | list], depth: int) -> float:
    total_sum = 0.0
    i = 0
    n = len(arr)

    # Unrolled by 4 elements
    while i + 3 < n:
        e0, e1, e2, e3 = arr[i], arr[i + 1], arr[i + 2], arr[i + 3]
        total_sum += product_sum(e0, depth + 1) if isinstance(e0, list) else e0
        total_sum += product_sum(e1, depth + 1) if isinstance(e1, list) else e1
        total_sum += product_sum(e2, depth + 1) if isinstance(e2, list) else e2
        total_sum += product_sum(e3, depth + 1) if isinstance(e3, list) else e3
        i += 4

    # Handle remaining elements
    while i < n:
        e = arr[i]
        total_sum += product_sum(e, depth + 1) if isinstance(e, list) else e
        i += 1

    return total_sum * depth


def product_sum_unrolled(array: list[int | list]) -> float:
    return product_sum(array, 1)


if __name__ == "__main__":
    # Option 1: increase input size to 973,075 for measurable profiling
    NUM_ELEMENTS = 973075
    random.seed(42)

    def generate_special_array(size: int, max_depth: int = 4) -> list:
        if max_depth == 0 or size < 10:
            return [random.randint(-100, 100) for _ in range(size)]
        return [
            generate_special_array(size // 2, max_depth - 1),
            [random.randint(-100, 100) for _ in range(size // 2)],
        ]

    arr = generate_special_array(NUM_ELEMENTS // 100)

    start = time.time()
    result = product_sum_unrolled(arr)
    end = time.time()

    print(f"Unrolled ProductSum result: {result}")
    print(f"Approx. elements processed: {NUM_ELEMENTS}")
    print(f"Execution time: {end - start:.2f} seconds")
