#!/usr/bin/env python3

import heapq
import sys
from collections import namedtuple

DIRECTIONS = (
    (+1,  0), # >
    ( 0, +1), # v
    (-1,  0), # <
    ( 0, -1), # ^
)

class Maze:
    def __init__(self, lines):
        self.start = None
        self.end = None
        self.walkable = set()
        for y, line in enumerate(lines):
            for x, char in enumerate(line.strip()):
                if char == '#':
                    continue
                elif char == '.':
                    pass
                elif char == 'S' and self.start is None:
                    self.start = x, y
                elif char == 'E' and self.end is None:
                    self.end = x, y
                else:
                    raise Exception("Unexpected input")
                self.walkable.add((x, y))

    def lowest_score(self):
        visited = set()
        def push(score, location, direction):
            state = location, direction
            if state not in visited:
                heapq.heappush(heap, (score, state))
        heap = [(0, (self.start, 0))]
        while item := heapq.heappop(heap):
            score, state = item
            location, direction = state
            if location == self.end:
                return score
            visited.add(state)
            x, y = location
            xd, yd = DIRECTIONS[direction]
            next_location = x + xd, y + yd
            if next_location in self.walkable:
                push(score+1, next_location, direction)
            push(score+1000, location, (direction+1)%4)
            push(score+1000, location, (direction+3)%4)

if __name__ == '__main__':
    maze = Maze(sys.stdin)
    part1 = maze.lowest_score()
    print(f"Part 1: {part1}")
