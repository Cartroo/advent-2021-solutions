#!/usr/bin/env python3.10

from enum import Enum
from itertools import count
from sys import stdin

class Cucumber(Enum):
    SPACE = 0
    EAST = 1
    SOUTH = 2

CUCUMBERS = {
    ">": Cucumber.EAST,
    "v": Cucumber.SOUTH
}

def find_moves(grid, x_axis, dim):
    if x_axis:
        target_type = Cucumber.EAST
        update_coord = lambda coord: ((coord[0] + 1) % dim[0], coord[1])
    else:
        target_type = Cucumber.SOUTH
        update_coord = lambda coord: (coord[0], (coord[1] + 1) % dim[1])
    for coord, cucumber in grid.items():
        if cucumber == target_type:
            new_coord = update_coord(coord)
            if new_coord not in grid:
                yield (new_coord, cucumber, True)
                continue
        yield (coord, cucumber, False)

grid = {}
max_x = max_y = 0
for y, row in enumerate(i.strip() for i in stdin):
    for x, char in enumerate(row):
        max_x = max(max_x, x)
        max_y = max(max_y, y)
        if char in CUCUMBERS:
            grid[(x, y)] = CUCUMBERS[char]
dim = (max_x + 1, max_y + 1)

for move_number in count():
    any_moved = False
    new_grid = {}
    for coord, cucumber, moved in find_moves(grid, True, dim):
        new_grid[coord] = cucumber
        any_moved = any_moved or moved
    grid = new_grid
    new_grid = {}
    for coord, cucumber, moved in find_moves(grid, False, dim):
        new_grid[coord] = cucumber
        any_moved = any_moved or moved
    grid = new_grid
    if not any_moved:
        print(f"Stable after {move_number + 1} steps")
        break
