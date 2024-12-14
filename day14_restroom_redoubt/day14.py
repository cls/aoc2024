#!/usr/bin/env python3

import math
import re
import statistics
import sys
from collections import namedtuple

Robot = namedtuple('Robot', ('position', 'velocity'))

def parse_robots(lines):
    pattern = re.compile(r'p=(\d+),(\d+) v=(-?\d+),(-?\d+)\n')
    for line in lines:
        match = pattern.fullmatch(line)
        if not match:
            raise Exception("Unexpected input")
        x, y, xd, yd = map(int, match.groups())
        yield Robot(position=(x, y), velocity=(xd, yd))

class Simulation:
    def __init__(self, dimensions):
        self.dimensions = dimensions

    def simulate_robot(self, robot, seconds):
        new_position = tuple((p + (v * seconds)) % d for p, v, d in zip(robot.position, robot.velocity, self.dimensions))
        return Robot(new_position, robot.velocity)

    def simulate_robots(self, robots, seconds):
        return (self.simulate_robot(robot, seconds) for robot in robots)

    def quadrant(self, robot):
        if any(p == (d // 2) for p, d in zip(robot.position, self.dimensions)):
            return None
        return sum(2 ** n if p > (d // 2) else 0 for n, (p, d) in enumerate(zip(robot.position, self.dimensions)))

    def count_quadrants(self, robots):
        counts = [0] * (2 ** len(self.dimensions))
        for quadrant in map(self.quadrant, robots):
            if quadrant is not None:
                counts[quadrant] += 1
        return counts

    def find_easter_egg(self, robots):
        def positional_deviation(seconds):
            unzipped_positions = zip(*(robot.position for robot in self.simulate_robots(robots, seconds)))
            return math.prod(map(statistics.pstdev, unzipped_positions))
        return min(range(math.prod(self.dimensions)), key=positional_deviation)

if __name__ == '__main__':
    robots = list(parse_robots(sys.stdin))
    #simulation = Simulation((11, 7))
    simulation = Simulation((101, 103))
    part1 = math.prod(simulation.count_quadrants(simulation.simulate_robots(robots, 100)))
    print(f"Part 1: {part1}")
    part2 = simulation.find_easter_egg(robots)
    print(f"Part 2: {part2}")
