#!/usr/bin/env python3

import itertools
import sys

DIRECTIONS = [
    ( 0, -1), # N
    (+1,  0), # E
    ( 0, +1), # S
    (-1,  0), # W
]

class Topography:
    def __init__(self, data):
        self.height_map = [[int(c) for c in line.strip()] for line in data]

    def __getitem__(self, location):
        x, y = location
        return self.height_map[y][x]

    def __iter__(self):
        for y, heights in enumerate(self.height_map):
            for x, height in enumerate(heights):
                yield (x, y), height

    def __contains__(self, location):
        x, y = location
        return y >= 0 and x >= 0 and y < len(self.height_map) and x < len(self.height_map[0])

    def neighbours(self, location):
        x, y = location
        for xd, yd in DIRECTIONS:
            neighbour = x + xd, y + yd
            if neighbour in self:
                yield neighbour

    def evaluate_trailheads(self, init, reducer):
        locations_by_height = {}
        for location, height in self:
            locations_by_height.setdefault(height, set()).add(location)
        value_by_location = {}
        for location in locations_by_height[9]:
            value_by_location[location] = init(location)
        for height in range(9, 0, -1):
            uphill = set(locations_by_height[height])
            for location in locations_by_height[height-1]:
                uphill_neighbours = (neighbour for neighbour in self.neighbours(location) if neighbour in uphill)
                value = reducer(value_by_location[neighbour] for neighbour in uphill_neighbours)
                value_by_location[location] = value
        return (value for location, value in value_by_location.items() if self[location] == 0)

if __name__ == '__main__':
    topography = Topography(sys.stdin)
    peaks = topography.evaluate_trailheads(lambda peak: {peak}, lambda peaks: set(itertools.chain.from_iterable(peaks)))
    part1 = sum(map(len, peaks))
    print(f"Part 1: {part1}")
    ratings = topography.evaluate_trailheads(lambda peak: 1, lambda ratings: sum(ratings))
    part2 = sum(ratings)
    print(f"Part 2: {part2}")
