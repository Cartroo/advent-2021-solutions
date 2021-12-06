#!/usr/bin/env python3.10

from math import prod
from sys import stdin

class Position:

    def __init__(self, horizontal=0.0, depth=0.0, aim=0.0):
        self._pos = complex(horizontal, depth)
        self._aim = aim

    def __str__(self):
        return f"Horizontal={self._pos.real} Depth={self._pos.imag} Aim={self._aim}"

    def command(self, command, arg):
        if command.lower() in ("up", "down"):
            self._aim += arg * (-1 if command.lower() == "up" else 1)
        elif command.lower() == "forward":
            self._pos += complex(arg, arg * self._aim)

    def product(self):
        return self._pos.real * self._pos.imag


position = Position()
for command, arg in (line.split() for line in stdin):
    position.command(command, int(arg))
print(position)
print(f"Product={position.product()}")

