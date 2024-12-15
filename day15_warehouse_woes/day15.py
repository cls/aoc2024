#!/usr/bin/env python3

import sys

class Warehouse:
    def __init__(self):
        self.robot = None
        self.boxes = set()
        self.walls = set()

    @staticmethod
    def parse(lines):
        warehouse = Warehouse()
        for y, line in enumerate(lines):
            line = line.strip()
            if not line:
                break
            for x, char in enumerate(line):
                if char == '.':
                    continue
                pos = x, y
                if char == 'O':
                    warehouse.boxes.add(pos)
                elif char == '#':
                    warehouse.walls.add(pos)
                elif char == '@':
                    warehouse.robot = pos
                else:
                    raise Exception("Unexpected input")
        return warehouse

    @staticmethod
    def step(pos, delta):
        return tuple(n + d for n, d in zip(pos, delta))

    def move_robot(self, delta):
        move = Warehouse.step(self.robot, delta)
        push = move
        while push in self.boxes:
            push = Warehouse.step(push, delta)
        if push not in self.walls:
            if move != push:
                self.boxes.remove(move)
                self.boxes.add(push)
            self.robot = move

    @staticmethod
    def gps(box):
        x, y = box
        return x + y*100

directions = {
    '^': ( 0, -1),
    '>': (+1,  0),
    'v': ( 0, +1),
    '<': (-1,  0),
}

if __name__ == '__main__':
    warehouse = Warehouse.parse(sys.stdin)
    for line in sys.stdin:
        for char in line.strip():
            warehouse.move_robot(directions[char])
    part1 = sum(warehouse.gps(box) for box in warehouse.boxes)
    print(f"Part 1: {part1}")
