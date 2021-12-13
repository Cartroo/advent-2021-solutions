#!/usr/bin/env python3.10

from itertools import count
from sys import stdin

class EnergyMap:

    def __init__(self, iterable):
        self.rows = list(iterable)
        self.total_squares = sum(len(i) for i in self.rows)

    def _all_squares(self):
        for y in range(len(self.rows)):
            for x in range(len(self.rows[y])):
                yield (x, y)

    def _neighbours(self, x, y):
        for ny in range(y-1, y+2):
            for nx in range(x-1, x+2):
                if ((ny == y and nx == x)
                    or not 0 <= ny < len(self.rows)
                    or not 0 <= nx < len(self.rows[ny])):
                    continue
                yield (nx, ny)

    def process_flashes(self):
        to_flash = set()
        # Increment step and note initial flashers
        for x, y in self._all_squares():
            self.rows[y][x] += 1
            if self.rows[y][x] == 10:
                to_flash.add((x, y))
        # Repeatedly process flashers until none left
        while True:
            try:
                flash_x, flash_y = to_flash.pop()
                for x, y in self._neighbours(flash_x, flash_y):
                    self.rows[y][x] += 1
                    if self.rows[y][x] == 10:
                        to_flash.add((x, y))
            except KeyError:
                break
        # Reset all flashed to zero
        flashes = 0
        for x, y in self._all_squares():
            if self.rows[y][x] > 9:
                self.rows[y][x] = 0
                flashes += 1

        return flashes

energy_map = EnergyMap([int(i) for i in line.strip()] for line in stdin)
for steps in count(1):
    if energy_map.process_flashes() == energy_map.total_squares:
        print(f"Steps={steps}")
        break
