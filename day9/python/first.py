#!/usr/bin/env python3.10

from collections import deque
from sys import stdin

class NeighbourChecker:

    def __init__(self):
        self.window = deque((None, None, None))

    def _neighbours(self, x):
        if self.window[0] is not None:
            yield self.window[0][x]
        if self.window[2] is not None:
            yield self.window[2][x]
        if x > 0:
            yield self.window[1][x-1]
        if x < len(self.window[1]) - 1:
            yield self.window[1][x+1]

    def find_local_minima(self, row):
        self.window.popleft()
        self.window.append(row)
        if self.window[1] is not None:
            for x in range(len(self.window[1])):
                value = self.window[1][x]
                if all(value < i for i in self._neighbours(x)):
                    yield value

checker = NeighbourChecker()
total_risk = 0
for row in ([int(i) for i in line.strip()] for line in stdin):
    total_risk += sum(i+1 for i in checker.find_local_minima(row))
else:
    total_risk += sum(i+1 for i in checker.find_local_minima(None))

print(f"Risk={total_risk}")