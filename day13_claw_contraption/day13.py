#!/usr/bin/env python3

import itertools
import numpy as np
import re
import sys
from collections import namedtuple

try:
    # Added in Python 3.12
    from itertools import batched
except ImportError:
    def batched(items, n):
        it = iter(items)
        while batch := tuple(itertools.islice(it, n)):
            yield batch

def parse_machines(lines):
    patterns = list(map(re.compile, [
        r'Button A: X\+(\d+), Y\+(\d+)\n',
        r'Button B: X\+(\d+), Y\+(\d+)\n',
        r'Prize: X=(\d+), Y=(\d+)\n',
        r'\n',
    ]))
    for batch in batched(lines, len(patterns)):
        matches = tuple(pattern.match(line) for line, pattern in zip(batch, patterns))
        if not all(matches):
            raise Exception("Unexpected input")
        button_a, button_b, prize, *_ = map(lambda match: tuple(map(int, match.groups())), matches)
        yield np.array((button_a, button_b)).T, np.array(prize)

def tokens_needed(machine):
    presses = solve_as_int(*machine) # np.linalg.solve loses too much float precision.
    if presses is None:
        return None
    prices = np.array((3, 1))
    tokens = np.dot(presses, prices)
    return tokens

def solve_as_int(matrix, vector):
    (a, b), (c, d) = matrix
    determinant = (a * d) - (b * c)
    if determinant == 0:
        raise np.linalg.LinAlgError("Singular matrix")
    adjugate = np.array(((d, -b), (-c, a)))
    numerator = adjugate @ vector
    if np.any(numerator % determinant):
        return None
    return numerator // determinant

def total_tokens_needed(machines):
    return sum(filter(None, map(tokens_needed, machines)))

if __name__ == '__main__':
    machines = list(parse_machines(sys.stdin))
    part1 = total_tokens_needed(machines)
    print(f"Part 1: {part1}")
    offset = 10000000000000
    part2 = total_tokens_needed((buttons, prize + offset) for buttons, prize in machines)
    print(f"Part 2: {part2}")
