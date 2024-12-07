#!/usr/bin/env python3

import sys

deltas = [
    ( 0, -1), # ^
    (+1,  0), # >
    ( 0, +1), # v
    (-1,  0), # <
]

def predict_path(position, obstructions, dimensions):
    x, y = position
    w, h = dimensions
    direction = 0
    while True:
        yield x, y, direction
        xd, yd = deltas[direction]
        new_x = x + xd
        new_y = y + yd
        if new_x < 0 or new_y < 0 or new_x >= w or new_y >= h:
            break
        if (new_x, new_y) in obstructions:
            direction = (direction + 1) % 4
        else:
            x, y = new_x, new_y

def do_part1(position, obstructions, dimensions):
    return len(set((x, y) for (x, y, _) in predict_path(position, obstructions, dimensions)))

def predict_opportunities(position, obstructions, dimensions):
    x, y = position
    w, h = dimensions
    direction = 0
    while True:
        xd, yd = deltas[direction]
        new_x = x + xd
        new_y = y + yd
        if new_x < 0 or new_y < 0 or new_x >= w or new_y >= h:
            break
        if (new_x, new_y) in obstructions:
            direction = (direction + 1) % 4
        else:
            yield new_x, new_y
            x, y = new_x, new_y

def do_part2(position, obstructions, dimensions):
    locations = set((x, y) for (x, y, _) in predict_path(position, obstructions, dimensions))
    locations.remove(position)
    count = 0
    for location in locations:
        obstructions.add(location)
        states = set()
        for state in predict_path(position, obstructions, dimensions):
            if state in states:
                count += 1
                break
            states.add(state)
        obstructions.remove(location)
    return count

if __name__ == '__main__':
    position = None
    obstructions = set()
    for y, line in enumerate(sys.stdin):
        for x, char in enumerate(line.strip()):
            if char == '.':
                pass
            elif char == '#':
                obstructions.add((x, y))
            elif char == '^':
                if position is not None:
                    raise Exception("More than one guard")
                position = (x, y)
            else:
                raise Exception("Unrecognised symbol")
    dimensions = (x+1, y+1)
    part1 = do_part1(position, obstructions, dimensions)
    print(f"Part 1: {part1}")
    part2 = do_part2(position, obstructions, dimensions)
    print(f"Part 2: {part2}")
