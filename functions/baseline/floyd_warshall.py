import math
import time


class Graph:
    def __init__(self, n=0):
        self.n = n
        self.dp = [
            [math.inf for _ in range(n)] for _ in range(n)
        ]

    def add_edge(self, u, v, w):
        self.dp[u][v] = w

    def floyd_warshall(self):
        for k in range(self.n):
            for i in range(self.n):
                for j in range(self.n):
                    self.dp[i][j] = min(self.dp[i][j], self.dp[i][k] + self.dp[k][j])


if __name__ == "__main__":
    NUM_NODES = 973075  # Large simulated workload for profiling

    start = time.time()
    total_nodes = 0

    # Simulate computational load
    for _ in range(NUM_NODES):
        total_nodes += 1

    end = time.time()

    print(f"Total nodes visited: {total_nodes} / {NUM_NODES}")
    print(f"Execution time: {end - start:.2f} s")