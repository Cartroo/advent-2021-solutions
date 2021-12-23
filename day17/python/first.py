#!/usr/bin/env python3.10

from itertools import count
from math import ceil
import re
from sys import stdin

TARGET_AREA_RE = re.compile("^\s*target area:\s*x=(?P<minx>-?\d+)\.+(?P<maxx>-?\d+)"
                            ",\s*y=(?P<miny>-?\d+)\.+(?P<maxy>-?\d+)\s*$")

target_area_match = TARGET_AREA_RE.match(stdin.readline())
target_x = (int(target_area_match.group("minx")), int(target_area_match.group("maxx")))
target_y = (int(target_area_match.group("miny")), int(target_area_match.group("maxy")))

# Brute force is sufficient for this problem.

def check_target(x_vel, y_vel, target_x, target_y):
    x_pos = y_pos = 0
    while x_pos <= target_x[1] and y_pos >= target_y[0]:
        if (x_pos >= target_x[0] and x_pos <= target_x[1] and
            y_pos >= target_y[0] and y_pos <= target_y[1]):
            return True
        x_pos += x_vel
        y_pos += y_vel
        if x_vel:
            x_vel -= x_vel / abs(x_vel)
        y_vel -= 1
    return False

possible_vels = set()
for init_x_vel in range(1, 200):
    for init_y_vel in range(200):
        if check_target(init_x_vel, init_y_vel, target_x, target_y):
            possible_vels.add((init_x_vel, init_y_vel))

y_vel, x_vel = max(possible_vels, key=lambda x: x[1])
max_height = (y_vel * (y_vel + 1)) // 2
print(f"Max height={max_height} y_vel={y_vel} x_vel={x_vel}")