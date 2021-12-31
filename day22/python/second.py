#!/usr/bin/env python3.10

import re
from sys import stdin
from typing import NamedTuple

# For speed I haven't been using type hints, but it's not appreciably
# slower to use typing.NamedTuple and it aids readability. I hope one
# day type hints will be so automatic to me that using them will
# actually be quicker than without (but I have many, many years of
# pre-type-hint Python habits to overcome!).
class Cuboid(NamedTuple):
    is_on: bool
    x_start: int
    x_end: int
    y_start: int
    y_end: int
    z_start: int
    z_end: int

    def get_volume(self):
        return ((self.x_end - self.x_start + 1) *
                (self.y_end - self.y_start + 1) *
                (self.z_end - self.z_start + 1))

# Feeling lazy, just parse input with a regex.
INPUT_RE = re.compile(r"^\s*(?P<onoff>on|off)\s+"
                      r"x=(?P<xstart>[-0-9]+)\.\.(?P<xend>[-0-9]+)\s*,\s*"
                      r"y=(?P<ystart>[-0-9]+)\.\.(?P<yend>[-0-9]+)\s*,\s*"
                      r"z=(?P<zstart>[-0-9]+)\.\.(?P<zend>[-0-9]+)\s*$")

def generate_input(fd):
    for line in fd:
        match = INPUT_RE.match(line)
        if match is not None:
            yield Cuboid(match.group("onoff") == "on",
                         int(match.group("xstart")),
                         int(match.group("xend")),
                         int(match.group("ystart")),
                         int(match.group("yend")),
                         int(match.group("zstart")),
                         int(match.group("zend")))

# The full cuboid covered by the input contains over 7e15 cubes, so tracking
# every one isn't an option. Instead we track a series of non-overlapping
# "on" cuboids, splitting them as needed.
#
# When adding an "OFF" cuboid, only overlaps with existing cuboids matter.
# When these are found, the existing one is split such that the remaining
# "on" area is a series of new non-overlapping cuboids. We split each
# cuboid into up to 6 other cuboids (skipping any which would have zero or
# negative volume):
# A: (x = ON.x_start..OFF.x_start) (y = as ON) (z = as ON)
# B: (x = overlap.x_start..overlap.x_end) (y = ON.y_start..OFF.y_start) (z = as ON)
# C: (x as previous) (y = overlap.y_start..overlap.y_end) (z = ON.z_start..OFF.z_start)
# D: (x as previous) (y = overlap.y_start..overlap.y_end) (z = OFF.z_end..ON.z_end)
# E: (x as previous) (y = OFF.y_end..ON.y_end) (z = as ON)
# F: (x = OFF.x_end..ON.x_end) (y = as ON) (z = as ON)
#
# When adding an "ON" cuboid, a similar process is followed, but the new
# cuboid is regarded as "ON" and the old one as "OFF" -- this yields a
# set of cuboids which capture any new cubes turned on by the new
# instruction.

def split_cuboid(on_cuboid, off_cuboid):
    # For splits to be required, the cuboids must overlap by at least
    # some extent in all dimensions.
    if not (on_cuboid.x_start <= off_cuboid.x_end and
            on_cuboid.x_end >= off_cuboid.x_start and
            on_cuboid.y_start <= off_cuboid.y_end and
            on_cuboid.y_end >= off_cuboid.y_start and
            on_cuboid.z_start <= off_cuboid.z_end and
            on_cuboid.z_end >= off_cuboid.z_start):
        yield on_cuboid
        return

    overlap_x_start = max(on_cuboid.x_start, off_cuboid.x_start)
    overlap_x_end = min(on_cuboid.x_end, off_cuboid.x_end)
    overlap_y_start = max(on_cuboid.y_start, off_cuboid.y_start)
    overlap_y_end = min(on_cuboid.y_end, off_cuboid.y_end)

    if on_cuboid.x_start < off_cuboid.x_start:
        yield Cuboid(True, on_cuboid.x_start, off_cuboid.x_start - 1,
                     on_cuboid.y_start, on_cuboid.y_end,
                     on_cuboid.z_start, on_cuboid.z_end)
    if on_cuboid.y_start < off_cuboid.y_start:
        yield Cuboid(True, overlap_x_start, overlap_x_end,
                     on_cuboid.y_start, off_cuboid.y_start - 1,
                     on_cuboid.z_start, on_cuboid.z_end)
    if on_cuboid.z_start < off_cuboid.z_start:
        yield Cuboid(True, overlap_x_start, overlap_x_end,
                     overlap_y_start, overlap_y_end,
                     on_cuboid.z_start, off_cuboid.z_start - 1)
    if on_cuboid.z_end > off_cuboid.z_end:
        yield Cuboid(True, overlap_x_start, overlap_x_end,
                     overlap_y_start, overlap_y_end,
                     off_cuboid.z_end + 1, on_cuboid.z_end)
    if on_cuboid.y_end > off_cuboid.y_end:
        yield Cuboid(True, overlap_x_start, overlap_x_end,
                     off_cuboid.y_end + 1, on_cuboid.y_end,
                     on_cuboid.z_start, on_cuboid.z_end)
    if on_cuboid.x_end > off_cuboid.x_end:
        yield Cuboid(True, off_cuboid.x_end + 1, on_cuboid.x_end,
                     on_cuboid.y_start, on_cuboid.y_end,
                     on_cuboid.z_start, on_cuboid.z_end)

# Yields only the new cuboids to add (if any).
def add_on_cuboid(previous, to_add):
    add_candidates = set((to_add,))
    for cuboid in previous:
        new_add_candidates = set()
        for candidate in add_candidates:
            new_add_candidates |= set(split_cuboid(candidate, cuboid))
        add_candidates = new_add_candidates
    yield from add_candidates    

# Yields the entire new list of cuboids after processing removals.
def add_off_cuboid(previous, to_remove):
    for cuboid in previous:
        yield from split_cuboid(cuboid, to_remove)

on_so_far = set()
for cuboid in generate_input(stdin):
    if cuboid.is_on:
        on_so_far |= set(add_on_cuboid(on_so_far, cuboid))
    else:
        on_so_far = set(add_off_cuboid(on_so_far, cuboid))

total_cubes = sum(i.get_volume() for i in on_so_far)
print(f"Total cubes on={total_cubes}")