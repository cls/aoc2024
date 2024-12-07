#!/usr/bin/env python3

import itertools
import operator
import sys

def possible_results(values, operators):
    for ops in itertools.product(operators, repeat=len(values)-1):
        it = iter(values)
        result = next(it)
        for op, value in zip(ops, it):
            result = op(result, value)
        yield result

def total_calibration(equations, operators):
    return sum(result for (result, values) in equations if result in possible_results(values, operators))

def append_numbers(x, y):
    return int(str(x) + str(y))

if __name__ == '__main__':
    equations = []
    for line in sys.stdin:
        lhs, rhs = line.split(':')
        equations.append((int(lhs), list(map(int, rhs.split()))))
    part1 = total_calibration(equations, [operator.add, operator.mul])
    print(f"Part 1: {part1}")
    part2 = total_calibration(equations, [operator.add, operator.mul, append_numbers])
    print(f"Part 2: {part2}")
