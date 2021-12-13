#!/usr/bin/env python3.10

from collections import deque
from math import prod
from sys import stdin

class HeightMap:

    def __init__(self, iterable):
        self.rows = list(iterable)

    def _neighbours(self, x, y):
        if y > 0:
            yield (x, y-1)
        if y < len(self.rows) - 1:
            yield (x, y+1)
        if x > 0:
            yield (x-1, y)
        if x < len(self.rows[y]) - 1:
            yield (x+1, y)

    def _neighbour_values(self, x, y):
        for nx, ny in self._neighbours(x, y):
            yield self.rows[ny][nx]

    def find_local_minima(self):
        for y in range(len(self.rows)):
            for x in range(len(self.rows[y])):
                value = self.rows[y][x]
                if all(value < i for i in self._neighbour_values(x, y)):
                    yield (x, y, value)

    def get_basin_size(self, x, y):
        to_check = set(((x, y),))
        checked = set()
        while True:
            try:
                point = to_check.pop()
                checked.add(point)
                for nx, ny in self._neighbours(*point):
                    if (nx, ny) not in checked and self.rows[ny][nx] < 9:
                        to_check.add((nx, ny))
            except KeyError:
                break
        return len(checked)

height_map = HeightMap([int(i) for i in line.strip()] for line in stdin)
basin_sizes = []
for x, y, value in height_map.find_local_minima():
    basin_sizes.append(height_map.get_basin_size(x, y))
print(f"Total basins={len(basin_sizes)} Top 3 product={prod(sorted(basin_sizes)[-3:])}")
