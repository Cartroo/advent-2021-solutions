#!/usr/bin/env python3.10

from itertools import pairwise
from sys import stdin

print(sum(1 for prev, curr in pairwise(int(j.strip()) for j in stdin) if curr > prev))

