#!/usr/bin/env python3.10

from collections import Counter
from itertools import pairwise
from sys import stdin

# With the larger number of iterations, the naive approach of tracking
# the polymer formula doesn't scale (gets too large too quickly). Since
# we only need the frequencies, however, and since the items added are
# independent, we can just track pair counts and derive the frequencies.
# To do this correctly needs the two ends being tracked specially, as
# these are the only cases where both items of the pair aren't shared
# with another.

class Formula:
    """Store formula as count of pairs.

    The first and last pair are stored in attributes `first` and `last`.
    Remaining (overlapping) pairs are stored in a Counter. As an example,
    the formula 'ABCBCD' would resolve into:
    - first = ('A', 'B')
    - last = ('C', 'D')
    - rest = Counter({('B', 'C'): 2, ('C', 'B'): 1})
    """

    def __init__(self, formula_str, transforms):
        self.first = formula_str[0], formula_str[1]
        self.rest = Counter(pairwise(formula_str[1:-1]))
        self.last = formula_str[-2], formula_str[-1]
        self.transforms = transforms

    def iterate(self):
        """Transform first & last, then rest.

        If the first and last transform, the additional character
        will push the old one into rest. We do all updates with a delta
        counter before applying, because each transformation in the
        row is meant to happen simultaneously with each other.
        """
        delta = Counter()
        # Handle first pair
        addition = transforms.get(self.first)
        if addition is not None:
            delta[(addition, self.first[1])] += 1
            self.first = (self.first[0], addition)
        # Handle last pair
        addition = transforms.get(self.last)
        if addition is not None:
            delta[(self.last[0], addition)] += 1
            self.last = (addition, self.last[1])
        # Handle remaining inner pairs
        for (first, second), count in self.rest.items():
            replacement = transforms.get((first, second))
            if replacement is not None:
                delta[(first, replacement)] += count
                delta[(replacement, second)] += count
                delta[(first, second)] -= count
        self.rest += delta

    def get_counts(self):
        counts = Counter()
        for (first, unused_second), count in self.rest.items():
            counts[first] += count
        counts[self.first[0]] += 1
        counts[self.last[0]] += 1
        counts[self.last[1]] += 1
        return counts

formula_str = stdin.readline().strip()
transforms = {}
for line in (i.strip() for i in stdin):
    if line:
        src, dst = (i.strip() for i in line.split("->", 1))
        transforms[tuple(src)] = dst

formula = Formula(formula_str, transforms)
for step in range(40):
    formula.iterate()

counts = formula.get_counts().most_common()
print(f"Most minus least common={counts[0][1]-counts[-1][1]}")
