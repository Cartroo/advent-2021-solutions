#!/usr/bin/env python3.10

import heapq
import re
from sys import stdin
from typing import NamedTuple

class PendingState(NamedTuple):
    # Cost must come first to create the correct sort order in the heap.
    cost: int
    state: tuple[tuple[int]]

class Move(NamedTuple):
    closing_move: bool
    amphipod: int
    src_col: int
    src_row: int
    dst_col: int
    dst_row: int

def check_win(state):
    return (state[2][1] == state[2][2] == 1 and
            state[4][1] == state[4][2] == 2 and
            state[6][1] == state[6][2] == 3 and
            state[8][1] == state[8][2] == 4)

# True iff there's a non-empty hallway space between the two columns.
def is_collision(state, src_col, dst_col):
    return any(state[i][0] for i in
               range(min(src_col, dst_col) + 1, max(src_col, dst_col)))

def find_moves_from_src(state, src_col, src_row, amphipod):
    # Consider all possible destination columns for this move.
    for dst_col, dst_stack in enumerate(state):
        if src_col == dst_col or is_collision(state, src_col, dst_col):
            continue
        # Find the deepest available space (if any)
        try:
            dst_row = len(dst_stack) - 1 - dst_stack[::-1].index(0)
        except ValueError:
            continue
        # Moves from hallway to room are only permitted if the destination
        # is the correct room for this amphipod.
        if dst_col == 2 * amphipod:
            # When moving to destination column, check it doesn't contain
            # any incorrect amphipods.
            if all(i == 0 or i == amphipod for i in dst_stack):
                yield Move(True, amphipod, src_col, src_row, dst_col, dst_row)
        # Consider moves into hallway from rooms.
        elif dst_col not in (2, 4, 6, 8) and src_col in (2, 4, 6, 8):
            # Check if destination is clear.
            if dst_stack[0] == 0:
                yield Move(False, amphipod, src_col, src_row, dst_col, dst_row)

def get_moves(state):
    # Consider all possible source columns for a move.
    moves = []
    for src_col, src_stack in enumerate(state):
        try:
            src_row, amphipod = [(n, i) for n, i in enumerate(src_stack) if i > 0][0]
        except IndexError:
            # This column is empty, so no possible moves.
            continue
        if src_col == 2 * amphipod and src_stack[1] == amphipod and src_stack[2] == amphipod:
            # This column is already in its target state
            continue
        moves.extend(find_moves_from_src(state, src_col, src_row, amphipod))
    if any(i.closing_move for i in moves):
        # If any closing moves, return just the first of them, since any
        # available closing move is automatically optimal.
        return [i for i in moves if i.closing_move][:1]
    else:
        # If no closing moves, return all possible moves.
        return moves

def move_amphipod(state, move):
    for col, stack in enumerate(state):
        if col == move.src_col:
            ret = list(stack)
            ret[move.src_row] = 0
            yield tuple(ret)
        elif col == move.dst_col:
            ret = list(stack)
            ret[move.dst_row] = move.amphipod
            yield tuple(ret)
        else:
            yield stack

# We use something like Dijkstra's algorithm, where we always pursue
# the path of least cost so far.
def greedy_solve(initial_state):
    # We need to use tuples to use as a key in best_cost below.
    initial_state = tuple(tuple(stack) for stack in initial_state)
    pending_heap = [PendingState(0, initial_state)]
    best_cost = {initial_state: 0}
    while pending_heap:
        # Pick the lowest-cost state to progress.
        unused_cost, state = heapq.heappop(pending_heap)
        best_cost_here = best_cost[state]
        if check_win(state):
            # This is a winning state, which must be the lowest cost one,
            # so return it immediately.
            return best_cost_here
        # Find available moves from the current state.
        for move in get_moves(state):
            steps = abs(move.dst_col - move.src_col) + move.src_row + move.dst_row
            new_cost = best_cost_here + 10 ** (move.amphipod - 1) * steps
            new_state = tuple(move_amphipod(state, move))
            # If this is lower cost than the current best route to that state,
            # replace the old one and add this new state as a new starting
            # point for searches.
            if best_cost.get(new_state, 99999) > new_cost:
                best_cost[new_state] = new_cost
                heapq.heappush(pending_heap, (new_cost, new_state))

def build_rooms(first_row, second_row):
    stacks = [[0] for i in range(11)]
    for row in (first_row, second_row):
        for num, stack_offset in enumerate(range(2, 9, 2)):
            stacks[stack_offset].append(row[num])
    return stacks

def read_input(fd):
    assert(fd.readline().strip() == "#############")
    assert(fd.readline().strip() == "#...........#")
    positions_re = re.compile("#([A-D])#([A-D])#([A-D])#([A-D])#")
    first_row = tuple(1 + ord(i) - ord("A") for i in positions_re.search(fd.readline()).groups())
    second_row = tuple(1 + ord(i) - ord("A") for i in positions_re.search(fd.readline()).groups())
    assert(fd.readline().strip() == "#########")
    return build_rooms(first_row, second_row)

initial_state = read_input(stdin)
print(greedy_solve(initial_state))