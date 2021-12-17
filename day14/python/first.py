#!/usr/bin/env python3.10

from collections import Counter
from itertools import pairwise
from sys import stdin

def process_insertions(formula, transforms):
    for first, second in pairwise(formula):
        yield first
        replacement = transforms.get((first, second))
        if replacement is not None:
            yield replacement
    yield second

formula = list(stdin.readline().strip())
transforms = {}
for line in (i.strip() for i in stdin):
    if line:
        src, dst = (i.strip() for i in line.split("->", 1))
        transforms[tuple(src)] = dst

for step in range(10):
    formula = list(process_insertions(formula, transforms))

counts = Counter(formula).most_common()
print(f"Most minus least common={counts[0][1]-counts[-1][1]}")
