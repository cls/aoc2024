#!/usr/bin/env python3

import itertools
import sys

def safety_check(record):
    all_increasing = None
    for x, y in itertools.pairwise(record):
        if x == y or abs(x - y) > 3:
            return False
        else:
            increasing = (x < y)
        if all_increasing is None:
            all_increasing = increasing
        elif all_increasing != increasing:
            return False
    return True

def dampened_safety_check(record):
    return safety_check(record) or any(safety_check(record[:i] + record[i+1:]) for i in range(len(record)))

if __name__ == '__main__':
    records = [list(map(int, line.split())) for line in sys.stdin]
    part1 = sum(safety_check(record) for record in records)
    print(f"Part 1: {part1}")
    part2 = sum(dampened_safety_check(record) for record in records)
    print(f"Part 2: {part2}")
