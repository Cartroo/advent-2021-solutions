#!/usr/bin/env python3.10

from sys import stdin

# It's fairly clear that the median value will be the optimum to minimise
# total displacement from the chosen point, so we just need to calculate
# that and then determine the total offset from it.

points = [int(i) for i in stdin.readline().split(",")]
median = sorted(points)[len(points)//2]
print(sum(abs(median-i) for i in points))

