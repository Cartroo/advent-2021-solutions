#!/usr/bin/env python3.10

from collections import Counter
from sys import stdin

set_bit_counter = Counter()
total_values = 0
for binary_str in (line.strip() for line in stdin):
    total_values += 1
    for offset in (o for o, v in enumerate(binary_str) if v == "1"):
        set_bit_counter[offset] += 1

gamma_str_list = ["0"] * (max(set_bit_counter.keys()) + 1)
for offset, count in set_bit_counter.items():
    if count > total_values / 2:
        gamma_str_list[offset] = "1"

gamma = int("".join(gamma_str_list), 2)
# Using the fact I know these are 12-bit numbers to simplify the code
epsilon = (~gamma & 0xFFF)

print(gamma * epsilon)

