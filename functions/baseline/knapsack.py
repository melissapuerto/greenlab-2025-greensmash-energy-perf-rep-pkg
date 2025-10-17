from __future__ import annotations
import random
import time
from functools import lru_cache


def knapsack(
    capacity: int,
    weights: list[int],
    values: list[int],
    counter: int,
    allow_repetition=False,
) -> int:
    @lru_cache
    def knapsack_recur(capacity: int, counter: int) -> int:
        if counter == 0 or capacity == 0:
            return 0

        if weights[counter - 1] > capacity:
            return knapsack_recur(capacity, counter - 1)
        else:
            left_capacity = capacity - weights[counter - 1]
            new_value_included = values[counter - 1] + knapsack_recur(
                left_capacity, counter - 1 if not allow_repetition else counter
            )
            without_new_value = knapsack_recur(capacity, counter - 1)
            return max(new_value_included, without_new_value)

    return knapsack_recur(capacity, counter)


if __name__ == "__main__":
    N = 50  # small enough to run recursive knapsack
    max_weight = 50
    max_value = 100
    capacity = 100
    random.seed(42) 

    weights = [random.randint(1, max_weight) for _ in range(N)]
    values = [random.randint(1, max_value) for _ in range(N)]

    start = time.time()
    result = knapsack(capacity, weights, values, len(values))
    end = time.time()

    print("Baseline knapsack max value:", result)
    print(f"Total items processed: {N}")
    print(f"Elapsed time: {end - start:.2f} s")
