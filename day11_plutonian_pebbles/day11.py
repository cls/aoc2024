#!/usr/bin/env python3

import math
import sys
from collections import defaultdict

def blink(stone):
    if stone == 0:
        return [1]
    digits = int(math.log10(stone)) + 1
    if digits % 2 == 0:
        split = 10 ** (digits // 2)
        return [stone // split, stone % split]
    return [stone * 2024]

def blinks(stones, count):
    quantities = defaultdict(int)
    for stone in stones:
        quantities[stone] += 1
    for n in range(count):
        new_quantities = defaultdict(int)
        for stone, quantity in quantities.items():
            for new_stone in blink(stone):
                new_quantities[new_stone] += quantity
        quantities = new_quantities
    return sum(quantities.values())

if __name__ == '__main__':
    stones = list(map(int, sys.stdin.read().split()))
    part1 = blinks(stones, 25)
    print(f"Part 1: {part1}")
    part2 = blinks(stones, 75)
    print(f"Part 2: {part2}")
