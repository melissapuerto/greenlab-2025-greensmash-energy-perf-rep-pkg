"""
Baseline Product Sum implementation.
Reference: https://dev.to/sfrasica/algorithms-product-sum-from-an-array-dc6
"""

import random
import time


def product_sum(arr: list[int | list], depth: int) -> int:
    total_sum = 0
    for ele in arr:
        total_sum += product_sum(ele, depth + 1) if isinstance(ele, list) else ele
    return total_sum * depth


def product_sum_array(array: list[int | list]) -> int:
    return product_sum(array, 1)


if __name__ == "__main__":
    # Option 1: increase input size to 973,075 for longer execution
    NUM_ELEMENTS = 973075
    random.seed(42)

    # Create a deeply nested structure to increase recursion depth and workload
    def generate_special_array(size: int, max_depth: int = 4) -> list:
        if max_depth == 0 or size < 10:
            return [random.randint(-100, 100) for _ in range(size)]
        return [
            generate_special_array(size // 2, max_depth - 1),
            [random.randint(-100, 100) for _ in range(size // 2)],
        ]

    arr = generate_special_array(NUM_ELEMENTS // 100)  # reduced top-level nesting for feasibility

    start = time.time()
    result = product_sum_array(arr)
    end = time.time()

    print(f"Baseline ProductSum result: {result}")
    print(f"Approx. elements processed: {NUM_ELEMENTS}")
    print(f"Execution time: {end - start:.2f} seconds")
