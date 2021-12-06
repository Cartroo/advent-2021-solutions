#!/usr/bin/env python3.10

from itertools import pairwise
from sys import stdin

# Lifted directly from itertools recipes
def triplewise(iterable):
    "Return overlapping triplets from an iterable"

    # triplewise('ABCDEFG') -> ABC BCD CDE DEF EFG
    for (a, _), (b, c) in pairwise(pairwise(iterable)):
        yield a, b, c

triples = triplewise(int(i.strip()) for i in stdin)
print(sum(1 for prev, curr in pairwise(triples) if sum(curr) > sum(prev)))

