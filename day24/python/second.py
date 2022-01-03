#!/usr/bin/env python3.10

import operator
from sys import stdin

class NoSolutionError(Exception):
    pass

OPERATIONS = {
    "add": operator.add,
    "mul": operator.mul,
    "div": operator.floordiv,
    "mod": operator.mod,
    "eql": lambda a, b: 1 if a == b else 0
}

class Registers:
    __slots__ = ("w", "x", "y", "z")

    def __init__(self, w=0, x=0, y=0, z=0):
        self.w, self.x, self.y, self.z = w, x, y, z

    @classmethod
    def clone(cls, other):
        return cls(other.w, other.x, other.y, other.z)

    def process_instruction(self, instr, out_a, in_a):
        try:
            in_a_value = int(in_a)
        except ValueError:
            in_a_value = getattr(self, in_a)
        out_a_value = getattr(self, out_a)
        value = OPERATIONS[instr](out_a_value, in_a_value)
        setattr(self, out_a, value)

# Track min/max values of registers.
class RegisterRange:
    __slots__ = ("w", "x", "y", "z")

    def __init__(self, reg):
        self.w, self.x, self.y, self.z = ((i, i) for i in (reg.w, reg.x, reg.y, reg.z))

    def process_instruction(self, instr, out_a, in_a):
        out1, out2 = getattr(self, out_a)
        try:
            in1 = in2 = int(in_a)
        except ValueError:
            in1, in2 = getattr(self, in_a)
        match instr:
            case "add":
                # Just add the minima and maxima.
                setattr(self, out_a, (out1+in1, out2+in2))
            case "mul":
                if out1 >= 0 and in1 >= 0:
                    # All values non-negative, so pairing is as addition.
                    setattr(self, out_a, (out1 * in1, out2 * in2))
                elif out2 <= 0 and in2 <= 0:
                    # If all values non-positive, result will be non-negative.
                    # Two most negative values provide the new maxima.
                    setattr(self, out_a, (out2 * in2, out1 * in1))
                elif out2 <= 0 and in1 >= 0:
                    # Mixed sign, pair most negative with least positive.
                    setattr(self, out_a, (out1 * in2, out2 * in1))
                elif out1 >= 0 and in2 <= 0:
                    setattr(self, out_a, (out2 * in1, out1 * in2))
                else:
                    # At least one range spans positive and negative, so
                    # we calculate all the possibilities.
                    possibles = [0, out1 * in1, out1 * in2, out2 * in1, out2 * in2]
                    setattr(self, out_a, (min(possibles), max(possibles)))
            case "div":
                if in1 == in2 == 0:
                    # We can't follow a path that leads to division by zero.
                    return False
                elif in1 >= 0:
                    setattr(self, out_a, (out1 // in2, out2 // (1 if in1 == 0 else in1)))
                elif in2 <= 0:
                    setattr(self, out_a, (out1 // in1, out2 // (-1 if in2 == 0 else in2)))
                else:
                    # If the denominator range spans zero, the new range is the negative
                    # and positive values of the most largest numerator in absolute terms.
                    max_num = max(abs(out1), abs(out2))
                    setattr(self, out_a, (-max_num, max_num))
            case "mod":
                if in1 == in2 == 0:
                    return False
                elif in1 == in2:
                    if out2 - out1 < in1 - 1 and out1 % in1 <= out2 % in2:
                        # Interval between values is less than the modulo, so
                        # can reduce the possible range of output.
                        setattr(self, out_a, (out1 % in1, out2 % in1))
                    else:
                        # Otherwise we use the full range of the modulo.
                        setattr(self, out_a, (0, in1 - 1))
                elif 0 < in1:
                    setattr(self, out_a, (0, in2 - 1))
                elif 0 > in2:
                    setattr(self, out_a, (in1 + 1, 0))
                else:
                    setattr(self, out_a, (in1 + 1, in2 - 1))
            case "eql":
                if out1 == out2 == in1 == in2:
                    setattr(self, out_a, (1, 1))
                elif out1 <= in2 and out2 >= in1:
                    setattr(self, out_a, (0, 1))
                else:
                    setattr(self, out_a, (0, 0))

def recurse_solution(program, reg, offset=0, digits_so_far=""):
    # Start with the largest digits.
    digit_range = range(1, 10)
    # Run through program code, recursing as necessary.
    for line_num, (instr, args) in enumerate(program[offset:]):
        if instr == "inp":
            next_offset = offset + line_num + 1
            for digit in digit_range:
                setattr(reg, args[0], digit)
                if not check_possible(program, next_offset, reg):
                    continue
                try:
                    return recurse_solution(program, Registers.clone(reg), next_offset, digits_so_far + str(digit))
                except NoSolutionError:
                    pass
            raise NoSolutionError()
        else:
            reg.process_instruction(instr, args[0], args[1])
    if reg.z == 0:
        return digits_so_far
    else:
        raise NoSolutionError()

# Do some min/max analysis to rule out branches of the search tree.
def check_possible(program, offset, reg):
    reg_range = RegisterRange(reg)
    for instr, args in program[offset:]:
        if instr == "inp":
            setattr(reg_range, args[0], (1, 9))
        else:
            reg_range.process_instruction(instr, args[0], args[1])
    return (reg_range.z[0] <= 0 <= reg_range.z[1])

def Tokeniser(fd):
    for instr, args in (i.strip().split(None, 1) for i in fd):
        yield (instr, args.split(None, 1))

program = list(Tokeniser(stdin))
solution = recurse_solution(program, Registers())
print(solution)