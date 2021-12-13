#!/usr/bin/env python3.10

from sys import stdin

total = 0
for digits, outputs in ((d_s.split(), o_s.split()) for d_s, o_s in (line.split("|", 1) for line in stdin)):
    total += sum(1 for i in outputs if len(i) in (2, 3, 4, 7))
print(f"Total={total}")

