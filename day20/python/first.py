#!/usr/bin/env python3.10

from sys import stdin

class Canvas:

    def __init__(self, rows):
        self.background = "0"
        self.rows = list(rows)
        self.origin = (0, 0)
        self.original_size = (len(self.rows[0]), len(self.rows))
        self.expand_canvas()

    def __str__(self):
        return "\n".join(row.replace("0", ".").replace("1", "#") for row in self.rows)

    def expand_canvas(self):
        background = self.background
        rows = self.rows
        origin_x, origin_y = self.origin
        empty = background * len(rows[0])
        if rows[0] != empty:
            rows.insert(0, empty)
            origin_y += 1
        if rows[1] != empty:
            rows.insert(0, empty)
            origin_y += 1
        if rows[-1] != empty:
            rows.append(empty)
        if rows[-2] != empty:
            rows.append(empty)
        prepend_columns = append_columns = 0
        if any(row[0] != background for row in self.rows):
            prepend_columns = 2
        elif any(row[1] != background for row in self.rows):
            prepend_columns = 1
        if any(row[-1] != background for row in self.rows):
            append_columns = 2
        elif any(row[-2] != background for row in self.rows):
            append_columns = 1
        if append_columns or prepend_columns:
            for i in range(len(rows)):
                rows[i] = background * prepend_columns + rows[i] + background * append_columns
            origin_x += prepend_columns

    def get_square(self, x, y):
        rows = self.rows
        assert(0 < x < len(rows[0]) - 1)
        assert(0 < y < len(rows) - 1)
        return "".join(rows[i][x-1:x+2] for i in range(y-1, y+2))

    def apply_algorithm(self, algorithm):
        if self.background == "0":
            new_background = algorithm[0]
        else:
            new_background = algorithm[511]
        print("NEW BACKGROUND =", new_background)
        rows = self.rows
        empty = new_background * len(rows[0])
        new_rows = [empty]
        for y in range(1, len(rows) - 1):
            new_row = new_background
            for x in range(1, len(rows[y]) - 1):
                value = int(self.get_square(x, y), 2)
                new_row += algorithm[value]
            new_row += new_background
            new_rows.append(new_row)
        new_rows.append(empty)
        self.rows = new_rows
        self.background = new_background
        self.expand_canvas()

    def count_pixels(self):
        return sum(row.count("1") for row in self.rows)

def convert(line):
    return line.strip().replace("#", "1").replace(".", "0")

algorithm = convert(stdin.readline())
canvas = Canvas(convert(line) for line in stdin if line.strip())
canvas.apply_algorithm(algorithm)
canvas.apply_algorithm(algorithm)
print(f"Lit pixels={canvas.count_pixels()}")

