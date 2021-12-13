#!/usr/bin/env python3.10

from collections import deque
from sys import stdin

BRACES = {"(": ")", "[": "]", "{": "}", "<": ">"}
POINTS = {")": 1, "]": 2, "}": 3, ">": 4}

points = []
for line in (i.strip() for i in stdin):
    stack = deque()
    for char in line:
        if char in BRACES.keys():
            stack.append(char)
        elif char != BRACES[stack.pop()]:
            break
    else:
        line_points = 0
        for completer in (BRACES[i] for i in reversed(stack)):
            line_points = line_points * 5 + POINTS[completer]
        points.append(line_points)
print(f"Median points={sorted(points)[len(points) // 2]}")
