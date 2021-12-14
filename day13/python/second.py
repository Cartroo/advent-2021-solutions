#!/usr/bin/env python3.10

from itertools import count
from sys import stdin

folds = []
points = set()
for line in (i.strip() for i in stdin):
    if not line:
        break
    x, y = (int(i) for i in line.split(",", 1))
    points.add((x, y))
for line in (i.strip() for i in stdin):
    items = line.split()
    assert(items[0] == "fold")
    assert(items[1] == "along")
    coord, amount = items[2].split("=", 1)
    folds.append((coord, int(amount)))

def fold_transform(points, fold):
    y_fold = (fold[0].lower() == "y")
    offset = fold[1]
    for x, y in points:
        if (y_fold and y > offset) or (not y_fold and x > offset):
            yield (x if y_fold else 2 * offset - x,
                   y if not y_fold else 2 * offset - y)
        else:
            yield (x, y)

folded_points = points
for fold in folds:
    folded_points = fold_transform(folded_points, fold)
folded_points = set(folded_points)

max_x = max(x for x, y in folded_points)
max_y = max(y for x, y in folded_points)
for row in range(max_y + 1):
    line = [" "] * (max_x + 1)
    for x, y in ((x, y) for x, y in folded_points if y == row):
        line[x] = "*"
    print("".join(line))
