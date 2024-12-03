#!/usr/bin/env python3

import re
import sys

def do_part1(data):
    pattern = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
    return sum(int(x) * int(y) for x, y in pattern.findall(data))

def do_part2(data):
    pattern = re.compile(r"do\(\)|don't\(\)|mul\((\d{1,3}),(\d{1,3})\)")
    total = 0
    do = True
    for match in pattern.finditer(data):
        text = match.group(0)
        if text == "do()":
            do = True
        elif text == "don't()":
            do = False
        elif do:
            x, y = match.group(1, 2)
            total += int(x) * int(y)
    return total

if __name__ == '__main__':
    data = sys.stdin.read()
    part1 = do_part1(data)
    print(f"Part 1: {part1}")
    part2 = do_part2(data)
    print(f"Part 2: {part2}")
