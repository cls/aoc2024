#!/usr/bin/env python3

import itertools
import sys

def fragmented_checksum(disk_map):
    files = disk_map[::2]
    holes = disk_map[1::2]
    checksum = 0
    disk_block = 0
    for file_id, file_size in enumerate(files):
        for file_block in range(file_size):
            checksum += file_id * disk_block
            disk_block += 1
        if file_id == len(files)-1:
            break
        for hole_block in range(holes[file_id]):
            compacted_file_id = len(files)-1
            if file_id == compacted_file_id:
                break
            compacted_file_size = files[compacted_file_id]
            compacted_file_size -= 1
            if compacted_file_size == 0:
                files.pop()
            else:
                files[compacted_file_id] = compacted_file_size
            checksum += compacted_file_id * disk_block
            disk_block += 1
    return checksum

def defragmented_checksum(disk_map):
    files = disk_map[::2]
    holes = disk_map[1::2]
    checksum = 0
    disk_block = 0
    for file_id, file_size in enumerate(files):
        if file_size < 0:
            disk_block -= file_size
        else:
            for file_block in range(file_size):
                checksum += file_id * disk_block
                disk_block += 1
        if file_id == len(files)-1:
            break
        hole_size = holes[file_id]
        try:
            while hole_size > 0:
                compacted_file_id = next(id for id in range(len(files)-1, file_id, -1) if 0 < files[id] <= hole_size)
                compacted_file_size = files[compacted_file_id]
                files[compacted_file_id] *= -1
                hole_size -= compacted_file_size
                for compacted_file_block in range(compacted_file_size):
                    checksum += compacted_file_id * disk_block
                    disk_block += 1
        except StopIteration:
            disk_block += hole_size
    return checksum

if __name__ == '__main__':
    disk_map = list(int(c) for c in sys.stdin.read().strip() if c.isdigit())
    part1 = fragmented_checksum(disk_map)
    print(f"Part 1: {part1}")
    part2 = defragmented_checksum(disk_map)
    print(f"Part 2: {part2}")
