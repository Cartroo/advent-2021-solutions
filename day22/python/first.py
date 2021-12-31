#!/usr/bin/env python3.10

import re
from sys import stdin
from typing import NamedTuple

# For speed I haven't been using type hints, but it's not appreciably
# slower to use typing.NamedTuple and it aids readability. I hope one
# day type hints will be so automatic to me that using them will
# actually be quicker than without (but I have many, many years of
# pre-type-hint Python habits to overcome!).
class CubeRange(NamedTuple):
    is_on: bool
    x_start: int
    x_end: int
    y_start: int
    y_end: int
    z_start: int
    z_end: int

# Feeling lazy, just parse input with a regex.
INPUT_RE = re.compile(r"^\s*(?P<onoff>on|off)\s+"
                      r"x=(?P<xstart>[-0-9]+)\.\.(?P<xend>[-0-9]+)\s*,\s*"
                      r"y=(?P<ystart>[-0-9]+)\.\.(?P<yend>[-0-9]+)\s*,\s*"
                      r"z=(?P<zstart>[-0-9]+)\.\.(?P<zend>[-0-9]+)\s*$")

def generate_input(fd):
    for line in fd:
        match = INPUT_RE.match(line)
        if match is not None:
            yield CubeRange(match.group("onoff") == "on",
                            int(match.group("xstart")),
                            int(match.group("xend")),
                            int(match.group("ystart")),
                            int(match.group("yend")),
                            int(match.group("zstart")),
                            int(match.group("zend")))

# For part one, a simple set suffices. 
cubes_on = set()
for cube_range in generate_input(stdin):
    for x in range(max(cube_range.x_start, -50), min(cube_range.x_end, 50) + 1):
        for y in range(max(cube_range.y_start, -50), min(cube_range.y_end, 50) + 1):
            for z in range(max(cube_range.z_start, -50), min(cube_range.z_end, 50) + 1):
                if cube_range.is_on:
                    cubes_on.add((x, y, z))
                else:
                    cubes_on.discard((x, y, z))
print(f"Cubes on={len(cubes_on)}")