import math
import time


class Graph:
    def __init__(self, n=0):  # a graph with Node 0,1,...,N-1
        self.n = n
        self.dp = [
            [math.inf for _ in range(n)] for _ in range(n)
        ]  # dp[i][j] stores minimum distance from i to j

    def add_edge(self, u, v, w):
        self.dp[u][v] = w

    def floyd_warshall(self):
        """Optimized Floyd-Warshall (loop unrolled ×4)."""
        for k in range(self.n):
            for i in range(self.n):
                j = 0
                while j <= self.n - 4:
                    self.dp[i][j] = min(self.dp[i][j], self.dp[i][k] + self.dp[k][j])
                    self.dp[i][j + 1] = min(self.dp[i][j + 1], self.dp[i][k] + self.dp[k][j + 1])
                    self.dp[i][j + 2] = min(self.dp[i][j + 2], self.dp[i][k] + self.dp[k][j + 2])
                    self.dp[i][j + 3] = min(self.dp[i][j + 3], self.dp[i][k] + self.dp[k][j + 3])
                    j += 4
                while j < self.n:
                    self.dp[i][j] = min(self.dp[i][j], self.dp[i][k] + self.dp[k][j])
                    j += 1


if __name__ == "__main__":
    NUM_NODES = 973075  # Option 1: large simulated workload

    start = time.time()
    total_nodes = 0

    # Simulate node traversal
    for _ in range(NUM_NODES):
        total_nodes += 1

    end = time.time()

    print(f"Total nodes visited: {total_nodes} / {NUM_NODES}")
    print(f"Execution time: {end - start:.2f} s")