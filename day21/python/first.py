#!/usr/bin/env python3.10

from itertools import count, zip_longest
from sys import stdin

def deterministic_die():
    for i in count():
        yield (i % 100) + 1

def sum_thrice(die):
    args = [iter(die)] * 3
    for values in zip_longest(*args):
        yield sum(values)

positions = [int(line.split(":", 1)[1].strip()) - 1 for line in stdin]
scores = [0] * len(positions)
rolls = 0
roller = sum_thrice(deterministic_die())
while max(scores) < 1000:
    for player in range(len(positions)):
        positions[player] = (positions[player] + next(roller)) % 10
        scores[player] += positions[player] + 1
        rolls += 3
        if scores[player] >= 1000:
            break

print(f"Rolls={rolls} Scores={scores} Answer={rolls * min(scores)}")
