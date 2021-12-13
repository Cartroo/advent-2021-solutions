#!/usr/bin/env python3.10

from collections import deque
from sys import stdin

BRACES = {"(": ")", "[": "]", "{": "}", "<": ">"}
POINTS = {")": 3, "]": 57, "}": 1197, ">": 25137}

points = 0
for line in (i.strip() for i in stdin):
    stack = deque()
    for char in line:
        if char in BRACES.keys():
            stack.append(char)
        elif char != BRACES[stack.pop()]:
            points += POINTS[char]
            break
print(f"Points={points}")