#!/usr/bin/env python3.10

from sys import stdin

# Making increased moves more expensive just changes the problem to
# use the mean instead of the median.

def triangular(n):
    return (n * (n+1)) / 2

points = [int(i) for i in stdin.readline().split(",")]
mean = int(sum(points) / len(points))
print(f"Mean={mean} Total fuel={sum(triangular(abs(i - mean)) for i in points)}")

