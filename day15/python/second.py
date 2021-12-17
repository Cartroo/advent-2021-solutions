#!/usr/bin/env python3.10

from collections import defaultdict
import heapq
from sys import stdin, stdout

class Grid:
    def __init__(self, rows):
        self.rows = list(rows)

    def neighbours(self, x, y):
        if y > 0:
            yield (x, y-1)
        if y < len(self.rows) - 1:
            yield (x, y+1)
        if x > 0:
            yield (x-1, y)
        if x < len(self.rows[y]) - 1:
            yield (x+1, y)

    # Standard Dijkstra's algorithm using a heap as a priority queue.
    def min_route(self, src, dst):
        # Initialise structures for tracking
        previous = {}
        src_entry = [0] + list(src)
        entries = {src: src_entry}
        unvisited = []
        visited = set()
        heapq.heappush(unvisited, src_entry)
        # Loop until dst is the lowest distance unvisted node.
        while unvisited:
            d, x, y = heapq.heappop(unvisited)
            if (x, y) == dst:
                break
            for nx, ny in self.neighbours(x, y):
                if (nx, ny) in visited:
                    continue
                new_d = d + self.rows[ny][nx]
                entry = entries.get((nx, ny))
                if entry is None:
                    entry = [new_d, nx, ny]
                    heapq.heappush(unvisited, entry)
                    entry[0] = new_d
                    entries[(nx, ny)] = entry
                    previous[(nx, ny)] = (x, y)
                elif new_d < entry[0]:
                    entry[0] = new_d
                    previous[(nx, ny)] = (x, y)
            visited.add((x, y))
            heapq.heapify(unvisited)

        return entries[dst][0]

rows = [list(int(i) for i in line) for line in (j.strip() for j in stdin)]
# Replicate horizontally
rows = [[(elem+i-1) % 9 + 1 for i in range(5) for elem in row] for row in rows]
# Replicate vertically
num_rows = len(rows)
for i in range(1, 5):
    for j in range(num_rows):
        rows.append([(elem+i-1) % 9 + 1 for elem in rows[j]])

grid = Grid(rows)
src = (0, 0)
dst = (len(grid.rows[len(grid.rows)-1]) - 1, len(grid.rows) - 1)
print(f"Shortest distance={grid.min_route(src, dst)}")
