#!/usr/bin/env python3

import sys

ALL_DIRECTIONS = [(xd, yd) for xd in (-1, 0, 1) for yd in (-1, 0, 1) if xd or yd]

def count_words(wordsearch, word):
    count = 0
    h = len(wordsearch)
    for y, line in enumerate(wordsearch):
        w = len(line)
        for x, char in enumerate(line):
            if char == word[0]:
                for xd, yd in ALL_DIRECTIONS:
                    if find_word(wordsearch, word, x, y, w, h, xd, yd):
                        count += 1
    return count

def find_word(wordsearch, word, x, y, w, h, xd, yd):
    for char in word:
        if x < 0 or x >= w or y < 0 or y >= h:
            return False
        if wordsearch[y][x] != char:
            return False
        x += xd
        y += yd
    return True

def count_x_words(wordsearch, word):
    count = 0
    h = len(wordsearch)
    for y, line in enumerate(wordsearch):
        if y == 0 or y + 1 >= h:
            continue
        w = len(line)
        for x, char in enumerate(line):
            if x == 0 or x + 1 >= w:
                continue
            if char == word[1]:
                diagonal1 = (wordsearch[y-1][x-1], wordsearch[y+1][x+1])
                diagonal2 = (wordsearch[y-1][x+1], wordsearch[y+1][x-1])
                valid_diagonals = ((word[0], word[2]), (word[2], word[0]))
                if diagonal1 in valid_diagonals and diagonal2 in valid_diagonals:
                    count += 1
    return count

if __name__ == '__main__':
    wordsearch = [line.strip().encode('ascii') for line in sys.stdin]
    part1 = count_words(wordsearch, b'XMAS')
    print(f"Part 1: {part1}")
    part2 = count_x_words(wordsearch, b'MAS')
    print(f"Part 2: {part2}")
