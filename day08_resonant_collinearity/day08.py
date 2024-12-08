#!/usr/bin/env python3

import itertools
import sys

def antinodes(antennae):
    for (ax, ay), (bx, by) in itertools.combinations(antennae, 2):
        xd = bx - ax
        yd = by - ay
        yield (ax - xd, ay - yd)
        yield (bx + xd, by + yd)

def do_part1(antennae_by_frequency, dimensions):
    w, h = dimensions
    unbounded_antinodes = itertools.chain.from_iterable(map(antinodes, antennae_by_frequency.values()))
    bounded_antinodes = ((x, y) for (x, y) in unbounded_antinodes if x >= 0 and x < w and y >= 0 and y < h)
    return len(set(bounded_antinodes))

def harmonic_antinodes(antennae, dimensions):
    w, h = dimensions
    for (ax, ay), (bx, by) in itertools.combinations(antennae, 2):
        xd = bx - ax
        yd = by - ay
        while ax >= 0 and ax < w and ay >= 0 and ay < h:
            yield ax, ay
            ax -= xd
            ay -= yd
        while bx >= 0 and bx < w and by >= 0 and by < h:
            yield bx, by
            bx += xd
            by += yd

def do_part2(antennae_by_frequency, dimensions):
    bounded_antinodes = itertools.chain.from_iterable(harmonic_antinodes(antennae, dimensions) for antennae in antennae_by_frequency.values())
    return len(set(bounded_antinodes))

if __name__ == '__main__':
    antennae_by_frequency = {}
    for y, line in enumerate(sys.stdin):
        for x, char in enumerate(line.strip()):
            if char == '.':
                pass
            elif char.isalnum():
                antennae_by_frequency.setdefault(char, []).append((x, y))
            else:
                raise Exception("unrecognised symbol")
    dimensions = (x+1, y+1)
    part1 = do_part1(antennae_by_frequency, dimensions)
    print(f"Part 1: {part1}")
    part2 = do_part2(antennae_by_frequency, dimensions)
    print(f"Part 2: {part2}")
