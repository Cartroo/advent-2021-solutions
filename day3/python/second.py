#!/usr/bin/env python3.10

from collections import Counter
from sys import stdin

oxygen_set = set(line.strip() for line in stdin)
co2_set = oxygen_set.copy()

def get_mcb(values, offset):
    count = sum(1 for i in values if i[offset] == "1")
    if count == len(values) - count:
        return "1"
    else:
        return "1" if count > (len(values) / 2) else "0"

for offset in range(0, 12):
    if len(oxygen_set) > 1:
        mcb = get_mcb(oxygen_set, offset)
        oxygen_set = {i for i in oxygen_set if i[offset] == mcb}
    if len(co2_set) > 1:
        mcb = get_mcb(co2_set, offset)
        co2_set = {i for i in co2_set if i[offset] != mcb}

oxygen_value = int(oxygen_set.pop(), 2)
co2_value = int(co2_set.pop(), 2)
print(f"Oxygen={oxygen_value} CO2={co2_value} Product={oxygen_value * co2_value}")

