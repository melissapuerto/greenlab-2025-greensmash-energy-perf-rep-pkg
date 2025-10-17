#!/usr/bin/python
"""
Optimized (Unroll-4) Breadth-First Search — scaled input (Option 1: 973075 nodes).
Reference baseline: Omkar Pathak BFS.
Optimizations:
  • Use collections.deque (no thread locks)
  • Unroll adjacency loop by 4
"""

from __future__ import annotations
from collections import deque
import time


class Graph:
    def __init__(self) -> None:
        self.vertices: dict[int, list[int]] = {}

    def add_edge(self, from_vertex: int, to_vertex: int) -> None:
        if from_vertex in self.vertices:
            self.vertices[from_vertex].append(to_vertex)
        else:
            self.vertices[from_vertex] = [to_vertex]

    def bfs(self, start_vertex: int) -> set[int]:
        visited = set()
        queue: deque[int] = deque([start_vertex])
        visited.add(start_vertex)

        while queue:
            vertex = queue.popleft()
            neighbors = self.vertices.get(vertex, [])
            n = len(neighbors)
            i = 0
            # Unroll 4 at a time
            while i + 3 < n:
                v0, v1, v2, v3 = neighbors[i:i + 4]
                if v0 not in visited:
                    visited.add(v0)
                    queue.append(v0)
                if v1 not in visited:
                    visited.add(v1)
                    queue.append(v1)
                if v2 not in visited:
                    visited.add(v2)
                    queue.append(v2)
                if v3 not in visited:
                    visited.add(v3)
                    queue.append(v3)
                i += 4
            while i < n:
                v = neighbors[i]
                if v not in visited:
                    visited.add(v)
                    queue.append(v)
                i += 1
        return visited


if __name__ == "__main__":
    NUM_NODES = 973075  # Option 1: large input graph
    g = Graph()

    # Create the same connected graph (chain)
    for i in range(NUM_NODES - 1):
        g.add_edge(i, i + 1)

    start = time.time()
    visited = g.bfs(0)
    end = time.time()

    print(f"Total nodes visited: {len(visited)} / {NUM_NODES}")
    print(f"Execution time: {end - start:.2f} s")
