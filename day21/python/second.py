#!/usr/bin/env python3.10

from sys import stdin
import time

PERMUTATIONS = { 3:1, 4:3, 5:6, 6:7, 7:6, 8:3, 9:1 }

# Since there are only 100 combinations of positions, x2 for either of two
# players going next, and only 7 possible transitions away from each of those
# states we can pre-compute all the permutations and treat this as a state
# machine. The state is based on the (player 1 pos, player 2 pos, current player).
state_machine = {}
for p0_pos in range(0, 10):
    for p1_pos in range(0, 10):
        for current_player in (0, 1):
            transitions = {}
            for roll, perms in PERMUTATIONS.items():
                if current_player == 0:
                    next_state = ((p0_pos + roll) % 10, p1_pos, 1)
                else:
                    next_state = (p0_pos, (p1_pos + roll) % 10, 0)
                transitions[roll] = (perms, next_state)
            state_machine[(p0_pos, p1_pos, current_player)] = transitions

def simulate(wins, universes, scores, state):
    for roll, (perms, next_state) in state_machine[state].items():
        new_universes = universes * perms
        if state[2] == 0:
            new_scores = (scores[0] + next_state[0] + 1, scores[1])
            if new_scores[0] > 20:
                wins[0] += new_universes
                continue
        else:
            new_scores = (scores[0], scores[1] + next_state[1] + 1)
            if new_scores[1] > 20:
                wins[1] += new_universes
                continue
        simulate(wins, new_universes, new_scores, next_state)


positions = tuple(int(line.split(":", 1)[1].strip()) - 1 for line in stdin)
wins = [0, 0]
simulate(wins, 1, (0, 0), (positions[0], positions[1], 0))
print(f"Player 1 wins={wins[0]} Player 2 wins={wins[1]} Max wins={max(wins)}")