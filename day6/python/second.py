#!/usr/bin/env python3.10

from collections import Counter
from sys import stdin

fish = Counter()

for value in (int(i) for i in stdin.readline().split(",")):
    fish[value] += 1

for day in range(256):
    breeding = fish[0]
    for i in range(max(fish.keys())):
        fish[i] = fish[i+1]
        fish[i+1] = 0
    fish[6] += breeding
    fish[8] += breeding

print(f"Total fish={sum(fish.values())}")

