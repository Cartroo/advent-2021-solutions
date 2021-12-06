#!/usr/bin/env python3.10

from collections import Counter
from sys import stdin

def cmp(a, b):
    return (a > b) - (a < b)

intersection_counter = Counter()
for line in stdin:
    start, end = ([int(j) for j in i.strip().split(",")] for i in line.split("->"))
    x_inc = cmp(end[0], start[0])
    y_inc = cmp(end[1], start[1])
    if x_inc * y_inc != 0:
        continue
    for i in range(max(abs(end[0] - start[0]), abs(end[1] - start[1])) + 1):
        intersection_counter[(start[0] + x_inc * i, start[1] + y_inc * i)] += 1

print(f"Intersections={sum(1 for v in intersection_counter.values() if v > 1)}")

