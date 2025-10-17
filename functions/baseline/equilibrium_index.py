"""
Baseline Equilibrium Index — scaled input (Option 1: 973075 elements).
"""

def equilibrium_index(arr: list[int]) -> int:
    total_sum = sum(arr)
    left_sum = 0

    for i, value in enumerate(arr):
        total_sum -= value
        if left_sum == total_sum:
            return i
        left_sum += value

    return -1


if __name__ == "__main__":
    import random
    import time

    ARRAY_SIZE = 973075  # Option 1: large input array
    # Random integers chosen within a moderate range to avoid overflow effects
    arr = [random.randint(-1000, 1000) for _ in range(ARRAY_SIZE)]

    start = time.time()
    eq_index = equilibrium_index(arr)
    end = time.time()

    print(f"Array size: {ARRAY_SIZE}")
    print(f"Equilibrium index: {eq_index}")
    print(f"Execution time: {end - start:.2f} s")
