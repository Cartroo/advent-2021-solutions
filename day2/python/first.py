#!/usr/bin/env python3.10

from sys import stdin

# Represent position as complex: real is horizontal, imaginary is depth
COMMANDS = {
    "forward": (1 + 0j),
    "down": (0 + 1j),
    "up": (0 - 1j)
}

position = (0 + 0j)
for command, arg in (line.split() for line in stdin):
    position += COMMANDS[command.lower()] * int(arg)
print(f"Horizontal={position.real} Depth={position.imag}")
print(f"Product={position.real * position.imag}")

