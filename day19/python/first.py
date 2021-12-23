#!/usr/bin/env python3.10

from collections import defaultdict
from math import radians, sin, cos
from sys import stdin

class Vector(tuple):

    def __add__(self, other):
        return Vector(self[i] + other[i] for i in range(len(self)))

    def __sub__(self, other):
        return Vector(self[i] - other[i] for i in range(len(self)))

class TransformMatrix:

    def __init__(self, rows):
        self.rows = rows

    def __mul__(self, other):
        this = self.rows
        if isinstance(other, TransformMatrix):
            that = other.rows
            output = []
            for y in range(len(this)):
                output_row = [(sum(this[y][i] * that[i][x] for i in range(len(this[0]))))
                              for x in range(len(that[0]))]
                output.append(output_row)
            return TransformMatrix(output)
        elif isinstance(other, Vector):
            return Vector(sum(this[y][i] * other[i] for i in range(len(other)))
                          for y in range(len(this)))
        else:
            raise NotImplementedError()

    def __str__(self):
        return repr(self.rows)

def RX(angle):
    angle = radians(angle)
    return TransformMatrix([[1, 0, 0],
                            [0, int(cos(angle)), int(-sin(angle))],
                            [0, int(sin(angle)), int(cos(angle))]])

def RY(angle):
    angle = radians(angle)
    return TransformMatrix([[int(cos(angle)), 0, int(sin(angle))],
                            [0, 1, 0],
                            [int(-sin(angle)), 0, int(cos(angle))]])

def RZ(angle):
    angle = radians(angle)
    return TransformMatrix([[int(cos(angle)), int(-sin(angle)), 0],
                            [int(sin(angle)), int(cos(angle)), 0],
                            [0, 0, 1]])

# We take the first scanner as defining our coordinate system, facing in the
# positive direction on the x-axis. This tuple defines all the transformations
# required to bring other facings in line with this one. Each scanner can be
# facing along one of the axes, in either a positive or negative direction,
# and for each of those there are four possible rotations around the axis at
# 0, 90, 180 and 270 degrees. I derived these using a right-handed coordinate
# system, although given that we're processing all possibilities I'm not sure
# it would make any difference to the end result.
ORIENTATIONS = (
    # Positive x-axis
    RX(0), RX(270), RX(180), RX(90),
    # Negative x-axis
    RZ(180), RZ(180) * RX(90), RZ(180) * RX(180), RZ(180) * RX(270),
    # Positive y-axis
    RZ(270), RX(270) * RZ(270), RX(180) * RZ(270), RX(90) * RZ(270),
    # Negative y-axis
    RZ(90), RX(90) * RZ(90), RX(180) * RZ(90), RX(270) * RZ(90),
    # Positive z-axis
    RY(90), RX(270) * RY(90), RX(180) * RY(90), RX(90) * RY(90),
    # Negative z-axis
    RX(180) * RY(270), RX(90) * RY(270), RY(270), RX(270) * RY(270)
)

transform_cache = dict()

def process_scanner(scanner, base_beacons, new_beacons):
    # We try the matching process at each orientation until we hit a match.
    for transform_id, transform in enumerate(ORIENTATIONS):
        # First we apply the current rotation to all new beacons.
        transformed_new = transform_cache.get((scanner, transform_id))
        if transformed_new is None:
            transformed_new = set(transform * vec for vec in new_beacons)
            transform_cache[(scanner, transform_id)] = transformed_new
        for to_check in transformed_new:
            for known_beacon in base_beacons:
                # We work out the translation if to_check is the same beacon
                # as known_beacon, and apply the same to all the other new
                # beacons and see how many matches we get.
                delta = known_beacon - to_check
                translated = set(vec + delta for vec in transformed_new)
                if len(translated & known_beacons) >= 12:
                    # We have found a match!
                    return translated
    # No match.
    return None

base_scanner = current_scanner = None
scanners = defaultdict(set)
for line in (i.strip() for i in stdin):
    if not line:
        continue
    elif line.startswith("--"):
        current_scanner = line.strip("-").strip()
        if base_scanner is None:
            base_scanner = current_scanner
    else:
        scanners[current_scanner].add(Vector(int(i) for i in line.split(",")))

found_scanners = {base_scanner: scanners[base_scanner]}

done_pairs = set()
while len(found_scanners) < len(scanners):
    progress = False
    for new_scanner, new_beacons in scanners.items():
        if new_scanner in found_scanners:
            continue
        for known_scanner, known_beacons in found_scanners.items():
            pair = (new_scanner, known_scanner)
            if pair in done_pairs:
                continue
            done_pairs.add(pair)
            result = process_scanner(new_scanner, known_beacons, new_beacons)
            if result is not None:
                found_scanners[new_scanner] = result
                progress = True
                print(f"Matched {new_scanner} with {known_scanner} ({len(found_scanners)} of {len(scanners)})")
                break
    if not progress:
        raise Exception("failed to match all scanners")

all_beacons = set().union(*(found_scanners.values()))
print(f"Beacons={len(all_beacons)}")
