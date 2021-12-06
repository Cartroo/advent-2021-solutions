#!/usr/bin/env python3.10

from sys import stdin

class Board:

    def __init__(self, rows):
        self.all_values = set()
        self.row_lines = []
        self.col_lines = None
        for row in ([int(i.strip()) for i in row.split()] for row in rows):
            self.row_lines.append(set(row))
            self.all_values.update(self.row_lines[-1])
            if self.col_lines is None:
                self.col_lines = [set() for i in row]
            for offset, value in enumerate(row):
                self.col_lines[offset].add(value)
        self.marked = set()

    def check_win(self, number):
        if number not in self.all_values:
            return False
        self.marked.add(number)
        for line in self.row_lines + self.col_lines:
            if len(line) == len(line & self.marked):
                return True

    def sum_unmarked(self):
        return sum(sum(i for i in line if i not in self.marked)
                   for line in self.row_lines)

draw_order = [int(i) for i in stdin.readline().split(",")]
boards = []
rows = []
for line in (i.strip() for i in stdin):
    if not line:
        if rows:
            boards.append(Board(rows))
            rows = []
        continue
    rows.append(line)
if rows:
    boards.append(Board(rows))

for draw in draw_order:
    for board in boards:
        if board.check_win(draw):
            board_sum = board.sum_unmarked()
            print(f"Draw={draw} Sum={board_sum} Product={draw * board_sum}")
            break
    else:
        continue
    break

