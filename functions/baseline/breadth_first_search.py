from __future__ import annotations
#!/usr/bin/python

"""Author: OMKAR PATHAK"""

from queue import Queue
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
        queue: Queue[int] = Queue()
        visited.add(start_vertex)
        queue.put(start_vertex)

        while not queue.empty():
            vertex = queue.get()
            for adjacent_vertex in self.vertices.get(vertex, []):
                if adjacent_vertex not in visited:
                    queue.put(adjacent_vertex)
                    visited.add(adjacent_vertex)
        return visited


if __name__ == "__main__":
    NUM_NODES = 973075  # Option 1: large input graph
    g = Graph()

    # Build a simple connected graph (chain) so BFS touches all vertices
    for i in range(NUM_NODES - 1):
        g.add_edge(i, i + 1)

    start = time.time()
    visited = g.bfs(0)
    end = time.time()

    print(f"Total nodes visited: {len(visited)} / {NUM_NODES}")
    print(f"Execution time: {end - start:.2f} s")
